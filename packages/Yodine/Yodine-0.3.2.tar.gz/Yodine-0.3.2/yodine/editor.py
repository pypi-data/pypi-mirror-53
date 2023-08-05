import sys, functools
import random
import trio
import os
import math
import pyglet
import pyglet.gl as pgl
import pyglet.window.mouse as pgmouse

from . import game
from .core.vector import Vector, ComponentVector
from .core.trig import fast_sin
from .core.entity import Entity, System, EntityTemplate, EventContext
from .core.extension import ModLoader
from pyglet.window import key
from tkinter import *
from tkinter import ttk
from typing import Optional

try:
    import simplejson as json

except ImportError:
    import json



class EditorToolkit(Frame):
    def __init__(self, editor, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.editor = editor
        self.grid(column=0, row=0, sticky=(N, W, E, S))

        self.init_widgets()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def add_component(self):
        nam = self.component_name.get()
        val = self.component_value.get()

        try:
            self.editor.extra_components[nam] = (json.loads(val) if val != '' else None)

        except json.JSONDecodeError:
            self.error.set('Component value is not JSON parseable!')

        else:
            self.component_name.set('')
            self.component_value.set('')
            self.error.set('')
            
            ttk.Label(self.component_list, text=nam, justify='right', font='Helvetica 12 bold').grid(row=len(self.editor.extra_components) - 1, column=0, sticky=(E,))

            e = ttk.Entry(self.component_list, text=val, justify='left')
            e.insert(0, val)
            e.configure(state='readonly')
            e.grid(row=len(self.editor.extra_components) - 1, column=1, sticky=(W,))

    def init_widgets(self):
        self.component_name = StringVar()
        self.component_value = StringVar()
        self.error = StringVar()
        
        cname = ttk.Entry(self, textvariable=self.component_name)
        cval = ttk.Entry(self, textvariable=self.component_value)

        ttk.Label(self, text='Component Name', justify='center').grid(row=0, column=0, sticky=(S,))
        ttk.Label(self, text='Component Value', justify='center').grid(row=0, column=1, sticky=(S,))

        cname.grid(row=1, column=0, sticky=(N,))
        cval.grid(row=1, column=1, sticky=(N,))

        button = ttk.Button(self, text='Add Component', command=self.add_component)
        button.grid(row=2, column=1, sticky=(N, W))

        error_lbl = ttk.Label(self, textvariable=self.error, justify='right', foreground='red')
        error_lbl.grid(row=2, column=0, sticky=(N, S, E))

        self.component_list = Frame(self, background='#DDD', height=350)
        self.component_list.grid(column=0, columnspan=2, row=3, rowspan=3, sticky='nswe')

        self.component_list.columnconfigure(0, weight=1)
        self.component_list.rowconfigure(0, weight=1)
        self.component_list.grid_propagate(0)


class Editor(game.Game):
    def __init__(self, game_name: str, database_file: Optional[str] = None):
        super().__init__(game_name, database_file)

        self.root = Tk()  
        self.root.title('Yoded Tools')
        self.frame = EditorToolkit(self, self.root, background='white')

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        self.running = False

        self.extra_components = {}

    def init_player(self):
        pass

    def stop(self):
        super().stop()
        self.running = False

    async def tk_loop(self):
        self.running = True

        while self.running:
            self.root.update_idletasks()
            self.root.update()
            
            await trio.sleep(1 / 15)

        self.root.destroy()

    async def loop(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(super().loop)
            nursery.start_soon(self.tk_loop)


def editor_plugin(loader: ModLoader):
    @loader.template
    class EditorCursor(EntityTemplate):
        name = 'edcursor'
        group = 'overlays'

        default_components = [
            ('position', (0, 0), 'VectorComponent'),
            ('cam', (0, 0), 'VectorComponent'),
            ('shown', False),
            ('age', 0),
            ('clickable', (35, 35), 'VectorComponent'),
            ('position', (0, 0), 'VectorComponent'),
            ('edcursor',),
            ('panspeed', 150),
        ]

    @loader.template
    class TilePaletteItem(EntityTemplate):
        name = 'edpaletteitem'
        group = 'overlays'

        default_components = [
            ('palette',),
            ('index', 0),
            ('tiletype',),
            ('clickable', (35, 35), 'VectorComponent'),
            ('position', (0, 0), 'VectorComponent'),
            ('selected', False),
            ('age', 0),
        ]

    
    @loader.template
    class ObjectPaletteItem(EntityTemplate):
        name = 'edobjpalette'
        group = 'overlays'

        default_components = [
            ('palette',),
            ('index', 0),
            ('template',),
            ('clickable', (35, 35)),
            ('position', (0, 0)),
            ('selected', False),
            ('age', 0),
        ]


    @loader.system_type
    class S_NormalRender(System):
        component_types = ['position', 'sprite']
        component_defaults = {'angle': 0}
        component_checks = {'render': 'normal'}

        def system_init(self):
            self.images = {}
            self.sprites = {}

            for r in self.manager.loader.routines['get.yodine.sprites']:
                self.images.update(r())

        def on_spawned(self, event: EventContext, sprite, **kwargs):
            entity = event.source
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])
            self.sprites[entity.id].rotation = -90

        def on_loaded(self, event: EventContext, sprite, **kwargs):
            entity = event.source
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])
            self.sprites[entity.id].rotation = -90

        def on_change_sprite(self, event: EventContext, new_sprite, **kwargs):
            entity = event.source

            if entity.id in self.sprites:
                self.sprites[entity.id].delete()

            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[new_sprite.value])
            self.sprites[entity.id].rotation = -90

        def render(self, entity: Entity, window: pyglet.window.Window, position, angle, sprite, **kwargs):
            if entity.id not in self.sprites:
                self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

            sprite = self.sprites[entity.id] # type: pyglet.sprite.Sprite

            vec = ComponentVector(position)
            newvec = Vector(entity.manager.camera_transform(window, vec.x, vec.y))

            sprite.x, sprite.y = newvec.x, newvec.y
            sprite.scale = self.manager.camera_zoom
            
            if 'localplayer' in entity:
                c_angle = -self.manager.camera_angle

            else:
                c_angle = self.manager.camera_angle

            sprite.rotation = -90 + math.degrees(angle.value + c_angle)

            if 'radius' in entity:
                rad = entity['radius'].value
                sprite.scale /= max(sprite.image.width, sprite.image.height) / rad

            if 'scale' in entity:
                scale = entity['scale'].value
                sprite.scale *= scale

            sprite.draw()



    def get_pos(entity: Entity, component_name: str = 'position') -> ComponentVector:
        assert component_name in entity
        return ComponentVector(entity[component_name])

    @loader.system_type
    class S_LabelRender(System):
        component_types = ['name', 'position']

        def render(self, entity: Entity, window: pyglet.window.Window, name, position, *args, **kwargs) -> None:
            pos = get_pos(entity)
            x, y = self.manager.camera_transform(window, *pos)
            y += 75

            label = pyglet.text.Label(
                name.value,
                anchor_x = 'center',
                anchor_y = 'center',
                x = x,
                y = y,
                bold = True
            )
            label.draw()


    @loader.system_type
    class S_EditorCursor(System):
        component_types = ['edcursor', 'position', 'shown', 'age', 'cam', 'panspeed']

        def tick(self, entity: Entity, dtime: float, age, cam, position, panspeed, shown, *args, **kwargs):
            self.keyboard = self.manager.game.keyboard

            age.value += dtime
            
            psp = panspeed
            panspeed = panspeed.value * dtime
            
            cam = ComponentVector(cam)
            position = ComponentVector(position)

            if self.keyboard[key.LSHIFT] or self.keyboard[key.RSHIFT]:
                shown.value = False
            
            else:
                shown.value = True

            if self.keyboard[key.UP]:
                cam.y += panspeed
                position.y += panspeed

            elif self.keyboard[key.DOWN]:
                cam.y -= panspeed
                position.y -= panspeed

            if self.keyboard[key.LEFT]:
                cam.x -= panspeed
                position.x -= panspeed

            elif self.keyboard[key.RIGHT]:
                cam.x += panspeed
                position.x += panspeed

            if self.keyboard[key.G]:
                psp.value += 10 * dtime

            if self.keyboard[key.F]:
                psp.value -= 10 * dtime
                psp.value = max(psp.value, 0.025)

            if self.keyboard[key.NUM_ADD]:
                entity.manager.camera_zoom += 0.2 * dtime
                entity.manager.camera_zoom = min(entity.manager.camera_zoom, 4)

            elif self.keyboard[key.NUM_SUBTRACT]:
                entity.manager.camera_zoom -= 0.2 * dtime
                entity.manager.camera_zoom = max(entity.manager.camera_zoom, 0.125)

            entity.manager.set_camera(cam.x, cam.y, 0)
            
        def on_mouse_move(self, event: EventContext, window, new_pos: Vector, pos_diff: Vector, position, shown, **kwargs):
            entity = event.source
            self.mouse_move(entity, window, new_pos, pos_diff, position, shown)

        def on_mouse_drag(self, event: EventContext, window, new_pos: Vector, pos_diff: Vector, _, _1, position, shown, **kwargs):
            entity = event.source
            self.mouse_move(entity, window, new_pos, pos_diff, position, shown)

        def mouse_move(self, entity: Entity, window, new_pos: Vector, pos_diff: Vector, position, shown, **kwargs):
            position = ComponentVector(position)

            nx, ny = entity.manager.un_camera_transform(window, new_pos.x, new_pos.y)

            position.x = nx
            position.y = ny

        def on_mouse_enter(self, event: EventContext, window, xy, shown, **kwargs):
            if self.keyboard and (self.keyboard[key.LSHIFT] or self.keyboard[key.RSHIFT]):
                shown.value = False
            
            else:
                shown.value = True

        def on_mouse_leave(self, event: EventContext, window, xy, shown, **kwargs):
            shown.value = False

        def render(self, entity: Entity, window: pyglet.window.Window, position, shown, age, **kwargs) -> None:
            if shown.value:
                position = ComponentVector(position)
                cx, cy = position.x, position.y

                wx = math.floor(cx / 35) * 35
                wy = math.floor(cy / 35) * 35

                wx, wy = entity.manager.camera_transform(window, wx, wy)

                wx = int(wx)
                wy = int(wy)

                color = (
                    255,
                    255,
                    20,
                    int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                )
                size = int(35 * self.manager.camera_zoom)

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        # position
                        wx,        wy,
                        wx + size, wy,
                        wx + size, wy + size,
                        wx,        wy + size,
                    )),

                    ('c4B', color * 4)
                )


    @loader.system_type
    class S_Clickables(System):
        component_types = ['clickable', 'position']
        component_defaults = {'down': 0}

        def inside(self, mousepos, position, clickable):
            pos = ComponentVector(position)
            cli = ComponentVector(clickable)

            return (
                mousepos.x > pos.x and mousepos.x <= pos.x + cli.x and
                mousepos.y > pos.y and mousepos.y <= pos.y + cli.y
            )

        def on_mouse_release(self, event, window, pos, button, modifiers, clickable, position, down):
            entity = event.source
            down = down.value

            if self.inside(pos, position, clickable):
                self.manager.emit(entity, 'click', pos, button, modifiers)
                down &= ~button

            entity['down'] = down


        def on_mouse_press(self, event, window, pos, button, modifiers, clickable, position, down):
            entity = event.source
            down = down.value

            if self.inside(pos, position, clickable):
                down |= button

            entity['down'] = down
        

        def render(self, entity: Entity, window: pyglet.window.Window, down, clickable, position, **kwargs) -> None:
            if down.value:
                position = ComponentVector(position)
                size = ComponentVector(clickable)

                color = (
                    40,
                    40,
                    40,
                    70,
                )

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        # position
                        int(position.x),          int(position.y),
                        int(position.x + size.x), int(position.y),
                        int(position.x + size.x), int(position.y + size.y),
                        int(position.x),          int(position.y + size.y),
                    )),

                    ('c4B', color * 4)
                )


    @loader.system_type
    class S_ObjectPalette(System):
        component_types = ['palette', 'index', 'template', 'selected', 'position', 'age', 'sprite']

        def system_init(self):
            self.selected = None
            self.images = {}
            self.sprites = {}
            self.spawned = []

            for r in self.manager.loader.routines['get.yodine.sprites']:
                self.images.update(r())

        def on_key_release(self, event, window,   button, modifiers,   selected, **kwargs):
            entity = event.source

            if selected.value and button == key.U and self.spawned:
                e = self.spawned.pop()
                e.remove()

        def on_spawned(self, event: EventContext, sprite, **kwargs):
            entity = event.source
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

        def on_loaded(self, event: EventContext, sprite, **kwargs):
            entity = event.source
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

        def on_change_sprite(self, event: EventContext, new_sprite, **kwargs):
            entity = event.source

            if entity.id in self.sprites:
                self.sprites[entity.id].delete()

            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[new_sprite.value])

        def tick(self, entity: Entity, dtime: float, age, *args, **kwargs):
            age.value += dtime

        def on_resetobjpalselect(self, event, **kwargs):
            entity = event.source
            entity['selected'].value = False

        def on_mouse_release(self, event, window,    xy, button, modifiers,    template, selected,   **kwargs):
            entity = event.source
            if button & pgmouse.LEFT and (modifiers & pyglet.window.key.MOD_SHIFT):
                self.put(entity, window, xy, template, selected)

        def on_click(self, event,    xy, button, modifiers,    template, selected,   **kwargs):
            entity = event.source
            if button & pgmouse.RIGHT:
                self.manager.emit_all('resetobjpalselect')
                entity['selected'].value = True
                self.selected = template.value

        def put(self, entity, window, xy, template, selected):
            if self.selected is not None and selected.value:
                tx, ty = self.manager.un_camera_transform(window, xy.x, xy.y)

                self.spawned.append(self.manager.current_level.create_templated_entity(self.selected, [
                    ('position', [tx, ty], 'VectorComponent'),
                    *list(self.manager.game.extra_components.items())
                ]))

                self.manager.game.extra_components = {}

                for child in self.manager.game.frame.component_list.winfo_children():
                    child.grid_remove()
        
        def render(self, entity: Entity, window,   index, template, selected, position, age, sprite,   **kwargs):
            if entity.id not in self.sprites:
                self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

            sprite = self.sprites[entity.id] # type: pyglet.sprite.Sprite
                
            wx = 10
            wy = window.height - 40 - index.value * 45

            pos = ComponentVector(position)
            pos.x, pos.y = wx, wy

            wx = int(wx)
            wy = int(wy)

            sprite.x, sprite.y = wx + 35 / 2, wy + 35 / 2
            sprite.scale = 35 / max(sprite.image.width, sprite.image.height)

            if 'scale' in entity:
                scale = entity['scale'].value
                sprite.scale *= scale

            sprite.draw()

            if selected.value:
                color = (
                    60,
                    230,
                    20,
                    int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                )

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        wx,      wy,
                        wx + 35, wy,
                        wx + 35, wy + 35,
                        wx,      wy + 35,
                    )),
                    ('c4B', color * 4)
                )
            

    @loader.system_type
    class S_TilePalette(System):
        component_types = ['palette', 'index', 'tiletype', 'selected', 'position', 'age']

        def system_init(self):
            self.selected = None
            self.start_pos = None
            self.curr_pos = None

        def tick(self, entity: Entity, dtime: float, age, *args, selected, **kwargs):
            age.value += dtime

        def on_resetpalselect(self, event, **kwargs):
            entity = event.source
            entity['selected'].value = False

        def on_mouse_release(self, event, window,    xy, button, modifiers,    tiletype, selected,   **kwargs):
            entity = event.source

            if button & pgmouse.LEFT and not (modifiers & (pyglet.window.key.MOD_SHIFT | pyglet.window.key.MOD_CTRL)) and not self.start_pos:
                self.put(entity, window, xy, tiletype, selected)

            if self.start_pos:
                if self.selected is not None and selected.value:
                    self.put_rectangle()
                            
                    self.start_pos = None
                    self.curr_pos = None

        def on_mouse_press(self, event, window,   xy, button, modifiers,  tiletype, selected,    **kwargs):
            entity = event.source

            if modifiers & pyglet.window.key.MOD_CTRL:
                tp = self.tile_pos(window, xy)
                self.start_pos = tp
                self.curr_pos = tp

        def on_mouse_drag(self, event, window,   xy, dxy, button, modifiers,   tiletype, selected,   **kwargs):
            entity = event.source

            if button & pgmouse.LEFT and not (modifiers & (pyglet.window.key.MOD_SHIFT | pyglet.window.key.MOD_CTRL)):
                self.put(entity, window, xy, tiletype, selected)

            elif self.start_pos:
                tp = self.tile_pos(window, xy)

                if modifiers & pyglet.window.key.MOD_CTRL:
                    self.curr_pos = tp

                else:
                    if self.selected is not None and selected.value:
                        self.put_rectangle()
                        
                        self.start_pos = None
                        self.curr_pos = None

        def tile_pos(self, window, vec):
            tx, ty = self.manager.un_camera_transform(window, *vec)

            tx = math.floor(tx / 35)
            ty = math.floor(ty / 35)

            return (tx, ty)

        def put_rectangle(self):
            x1, y1 = self.start_pos
            x2, y2 = self.curr_pos

            if x1 > x2:
                x2, x1 = x1, x2

            if y1 > y2:
                y2, y1 = y1, y2

            self.manager.current_level.rectangle(Vector((x1, y1)), x2 - x1 + 1, y2 - y1 + 1, self.selected)

        def on_click(self, event,    xy, button, modifiers,    tiletype, selected,   **kwargs):
            entity = event.source

            if button & pgmouse.RIGHT:
                self.manager.emit_all('resetpalselect')
                entity['selected'].value = True
                self.selected = tiletype.value

        def put(self, entity, window, xy, tiletype, selected):
            if self.selected is not None and selected.value:
                tx, ty = self.tile_pos(window, xy)

                if (tx, ty) not in self.manager.current_level.tiles or self.manager.current_level.tiles[tx, ty] != self.selected:
                    self.manager.current_level.set(Vector((tx, ty)), self.selected)
        
        def render(self, entity: Entity, window,   index, tiletype, selected, position, age,   **kwargs):
            wx = window.width - 40
            wy = window.height - 40 - index.value * 45
            entity.manager.force_render_tile(window, tiletype.value, wx, wy)
            position.value = [wx, wy]

            if selected.value:
                color = (
                    20,
                    60,
                    255,
                    int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                )

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        wx,      wy,
                        wx + 35, wy,
                        wx + 35, wy + 35,
                        wx,      wy + 35,
                    )),

                    ('c4B', color * 4)
                )

                if self.start_pos:
                    sp = self.manager.camera_transform(window, *(Vector(self.start_pos) * 35)).ints()
                    cp = (self.manager.camera_transform(window, *(Vector(self.curr_pos) * 35))).ints()

                    if sp.x > cp.x:
                        sp.x, cp.x = cp.x, sp.x

                    if sp.y > cp.y:
                        sp.y, cp.y = cp.y, sp.y

                    cp += self.manager.camera_transform_delta(window, 35, 35)
                    cp = cp.ints()

                    color = (
                        200,
                        75,
                        75,
                        int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                    )

                    pyglet.graphics.draw(4, pgl.GL_QUADS,
                        ('v2i', (
                            sp.x, sp.y,
                            cp.x, sp.y,
                            cp.x, cp.y,
                            sp.x, cp.y,
                        )),

                        ('c4B', color * 4)
                    )

    @loader.system_type
    class S_FPSCounter(System):
        component_types = ['fpscounter']

        def render(self, entity: Entity, window: pyglet.window.Window, *args, **kwargs) -> None:
            if hasattr(self, 'dtime'):
                label = pyglet.text.Label(
                    str(round(1 / self.dtime, 1)),
                    x = 30,
                    y = 30,
                    bold = True
                )
                label.draw()

        def tick(self, entity: Entity, dtime: float, *args, **kwargs):
            self.dtime = dtime

    @loader.system_type
    class S_SizeRandom(System):
        component_types = ['sizerandom']

        def on_spawned(self, event: EventContext, sizerandom, **kwargs):
            entity = event.source
            
            entity['radius'].value = entity['radius'].value + random.uniform(-entity['sizerandom'].value, entity['sizerandom'].value)


    @loader.system_type
    class S_Readable(System):
        component_types = ['message', 'position']

        def render(self, entity: Entity, window: pyglet.window.Window, position, message, **kwargs):
            pos = ComponentVector(position)
            dist = (self.manager.camera - pos).vsize()

            if dist < 150:
                alpha = 1 - dist / 150

                pos = get_pos(entity)
                x, y = self.manager.camera_transform(window, *pos)
                y += 60

                label = pyglet.text.Label(
                    message.value,
                    anchor_x = 'center',
                    anchor_y = 'center',
                    x = x,
                    y = y,
                    bold = True,
                    font_size=14 * self.manager.camera_zoom,
                    color=(190, 130, 30, int(255 * alpha)),
                    multiline=True,
                    width=window.width * 3 / 5,
                    align='center',
                )
                label.draw()


    @loader.system_type
    class S_AngleRandom(System):
        component_types = ['anglerandom']

        def on_spawned(self, event: EventContext, **kwargs):
            entity = event.source
            entity['angle'].value = random.uniform(0, math.pi * 2)

    @loader.routine('preload.Yoded')
    def editor_preinit(game: Editor):
        manag = game.manager
        manag.systems = []

    @loader.routine('postload.Yoded')
    def editor_init(game: Editor):
        manag = game.manager

        for e in manag:
            if 'edcursor' in e or 'palette' in e:
                e.remove()

        manag.create_templated_entity('edcursor', [
            ('cshown', True)
        ])

        for i, tt in enumerate(manag.tile_types.keys()):
            manag.create_templated_entity('edpaletteitem', [
                ('index', i),
                ('tiletype', tt)
            ])

        i = 0
        for tname, template in manag.templates.items():
            if hasattr(template, 'editor_visible') and template.editor_visible:
                manag.create_templated_entity('edobjpalette', [
                    ('index', i),
                    ('sprite', template.get_value('sprite')),
                    ('template', tname)
                ])
                i += 1

        print("Editor initialized successfully.")


def editor_main():
    editor = Editor(os.environ.get('YODINE_GAME', 'yodine_data'), sys.argv[1] if len(sys.argv) > 1 else 'main.save.json')

    if len(sys.argv) > 2:
        lid = sys.argv[2]

        if lid in editor.manager.levels:
            editor.manager.change_level(lid)

        else:
            editor.manager.create_level(lid)

    editor.manager.apply_mod('Yoded', editor_plugin)

    print('Starting Editor...')
    editor.run()


if __name__ == '__main__':
    editor_main()