import sqlite3
import uuid
import collections
import traceback
import warnings
import math
import json
import pyglet
import typing
import itertools

from typing import Optional, Iterable, Any, Tuple, TypeVar, Type, Iterator, Union, Callable, Dict
from .extension import ModLoader
from .vector import Vector, ComponentVector
from pyglet import gl



CIRCUM_MUL = 2 / math.sqrt(2)

ComponentType = Type['Component']



class EventContext(object):
    def __init__(self, name, manager, source, local = None, **kwargs):
        self.name = name
        self.manager = manager
        self.game = manager.game
        self.source = source

        self.local = local or self.game.id

        for attr_name, attr_value in kwargs.items():
            setattr(self, attr_name, attr_value)


class EntityContainer(object):
    def __init__(self):
        self.entity_component_index = {} # dict[entity => dict[component name => A implements Component]]
        self.entity_ids = [] # list<entity id>
        self.entity_id_set = set() # set<entity id>
        self.entity_count = 0

    def get_entities(self):
        return EntityContainer.__iter__(self)

    def get_component_types(self):
        return self.component_types

    def __len__(self):
        return self.entity_count

    def __iter__(self) -> Iterator['Entity']:
        return (Entity(self, eid) for eid in self.entity_ids)

    def load_entity(self, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        if not identifier:
            identifier = str(uuid.uuid4())
            
        e = Entity(self, identifier)

        getattr(self, 'manager', self).register_delta('crt', identifier, getattr(self, 'id', None))

        for c in components:
            e.create_component(*c)
            
        getattr(self, 'manager', self).emit(e, 'loaded')

        return e

    def create_entity(self, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = self.load_entity(components, identifier)

        getattr(self, 'manager', self).emit_all('spawn', e)
        getattr(self, 'manager', self).emit(e, 'spawned')

        return e

    def create_templated_entity(self, template_name: str, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = self.templates[template_name]
        ent = e.spawn(self, components, identifier)
        
        return ent

    def remove_entity(self, e: 'Entity') -> None:
        if e.level is self:
            e.remove()


# === Level data ===

class TileType(object):
    name = None # type: str
    post = False

    def __init__(self, sprite: pyglet.resource.image, name: Optional[str] = None):
        self.image = sprite.get_texture()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)   

        size = 35

        self.image.width = size
        self.image.height = size
        self.image.anchor_x = size / 2
        self.image.anchor_y = size / 2

        self.sprite_cache = {} # type: Dict[Tuple[int, int], pyglet.sprite.Sprite]
        self.post_sprite_cache = {} # type: Dict[Tuple[int, int], pyglet.sprite.Sprite]

        if name:
            self.name = name

        else:
            self.name = type(self).name

    def unset(self, level: 'Level', x, y):
        if (x, y) in self.sprite_cache:
            self.sprite_cache[x, y][1].delete()
            del self.sprite_cache[x, y]

        if (x, y) in self.post_sprite_cache:
            self.post_sprite_cache[x, y][1].delete()
            del self.post_sprite_cache[x, y]

    def force_render_tile(self, window: pyglet.window.Window, level: 'Level', wx, wy):
        pyglet.sprite.Sprite(self.image, wx + 35 / 2, wy + 35 / 2).draw()

    def _render(self, window: pyglet.window.Window, level: 'Level', x, y, wx, wy, cam_angle, cam_zoom, batch = None, cache = None):
        if self.image:
            cache = cache if cache is not None else self.sprite_cache

            if (x, y) in cache:
                ow, sprite = cache[x, y]
                sprite.visible = True

                try:
                    sprite.rotation = math.degrees(cam_angle)
                    sprite.scale = cam_zoom
            
                    if (wx, wy) != ow:
                        sprite.position = (wx, wy)

                except AttributeError as err:
                    print("WARNING: Bad tile sprite found at x={},y={} (see error below); deleting and ignoring.".format(x, y))
                    traceback.print_exc()

                    if (x, y) in cache:
                        del cache[x, y]

                    return

            else:
                sprite = pyglet.sprite.Sprite(self.image, wx, wy, batch=batch or level.batch)
                cache[x, y] = ((wx, wy), sprite)

    def render(self, window: pyglet.window.Window, level: 'Level', x, y, wx, wy, cam_angle, cam_zoom):
        if not self.post:
            self._render(window, level, x, y, wx, wy, cam_angle, cam_zoom)

    def post_render(self, window: pyglet.window.Window, level: 'Level', x, y, wx, wy, cam_angle, cam_zoom):
        if self.post:
            self._render(window, level, x, y, wx, wy, cam_angle, cam_zoom, level.post_batch, self.post_sprite_cache)
        
    def unrender(self, window: pyglet.window.Window, level: 'Level', x, y, wx, wy, cam_angle, cam_zoom):
        if (x, y) in self.sprite_cache:
            _, s = self.sprite_cache[x, y] # type: pyglet.sprite.Sprite
            s.visible = False

    def post_unrender(self, window: pyglet.window.Window, level: 'Level', x, y, wx, wy, cam_angle, cam_zoom):
        if (x, y) in self.post_sprite_cache:
            _, s = self.post_sprite_cache[x, y] # type: pyglet.sprite.Sprite
            s.visible = False

    def tick(self, manager: 'Manager', *args):
        pass

    def is_inside(self, manager: 'Manager', ent: 'Entity') -> bool:
        if 'position' not in ent:
            return False

        vec = ComponentVector(ent['position'])
        x = math.floor(vec.x / 35)
        y = math.floor(vec.y / 35)
        
        return manager.current_level.tiles.get((x, y), None) == self.name
        
    def _on(self, event_name: str, event: EventContext, *args, **kwargs):
        if hasattr(self, 'on_' + event_name):
            return getattr(self, 'on_' + event_name)(event, *args, **kwargs)

class Trigger(object):
    def __init__(self, level: EntityContainer, x, y, width = 1, height = 1):
        self.level = level
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.inside = set()

    def is_inside(self, ent: 'Entity') -> bool:
        if 'position' not in ent:
            return False

        left = self.x * 35
        right = (self.x + self.width) * 35
        top = self.y * 35
        bottom = (self.y + self.height) * 35

        vec = ComponentVector(ent['position'])
        
        return vec.x >= left and vec.x <= right and vec.y >= top and vec.y <= bottom

    def tick(self, *args):
        for e in self.level.manager:
            if self.is_inside(e):
                if e not in self.inside:
                    self.inside.add(e)
                    self.triggered(e)

            elif e in self.inside:
                self.inside.remove(e)
    


# === Entity Component System ===



class Level(EntityContainer):
    def __init__(self, lid  : str, manager: 'Manager'):
        EntityContainer.__init__(self)
    
        self.id = lid
        self.manager = manager
        self.tiles = {}
        self.deltas = []

        self.batch = pyglet.graphics.Batch()
        self.post_batch = pyglet.graphics.Batch()
        self.last_rendered = set()

    def __iter__(self) -> Iterator['Entity']:
        for e in self.get_entities():
            yield e

        for e in self.manager.get_entities():
            yield e

    def emit(self, source, event_name, *args):
        return self.manager.emit(source, event_name, *args)

    def create_templated_entity(self, template_name: str, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = self.manager.templates[template_name]
        ent = e.spawn(self, components, identifier)
        
        return ent

    def get_component_types(self):
        return self.manager.get_component_types()

    def entities_at(self, x: int, y: int) -> Iterator['Entity']:
        left = x * 35
        right = (x + 1) * 35

        top = y * 35
        bottom = (y + 1) * 35

        for e in self.get_entities():
            if 'position' in e:
                pos = ComponentVector(e['position'])

                if pos.x >= left and pos.x <= right and pos.y >= top and pos.y <= bottom:
                    yield e

                del pos

    def tiles(self, tt: TileType) -> Iterator[Vector]:
        for xy, tile in self.tiles.items():
            if tile == tt.name:
                yield Vector(xy)

    def transform_position(self, vec: Vector) -> Vector:
        return type(vec)(int(vec.x / 35), int(vec.y / 35))

    def rectangle(self, start: Vector, width: int, height: int, tile: str):
        for y in range(int(start.y), int(start.y) + height):
            for x in range(int(start.x), int(start.x) + width):
                if (x, y) in self.tiles and self.tiles[x, y] != tile:
                    self.manager.tile_types[self.tiles[x, y]].unset(self, x, y)

                self.tiles[x, y] = tile

        self.deltas.append(('rect', int(start.x), int(start.y), width, height, tile))

    def set(self, pos: Vector, tile: str):
        if (int(pos.x), int(pos.y)) in self.tiles:
            if self.tiles[int(pos.x), int(pos.y)] == tile:
                return

            self.manager.tile_types[self.tiles[int(pos.x), int(pos.y)]].unset(self, int(pos.x), int(pos.y))

        self.tiles[int(pos.x), int(pos.y)] = tile
        self.deltas.append(('set', int(pos.x), int(pos.y), tile))

    def save(self):
        return json.dumps(self.get_save())

    def get_save(self):
        return {
            'deltas': self.deltas
        }

    def load(self, data: str):
        self.load_save(json.loads(data))

    def load_save(self, save):
        self.deltas = []

        deltas = list(save['deltas'])

        self.tiles = {}

        for i, d in enumerate(deltas):
            if d not in deltas[i + 1:]:
                self.apply_delta(d)

    def apply_delta(self, d):
        kind = d[0]

        if kind == 'set':
            self.set(Vector((d[1], d[2])), *d[3:])

        elif kind == 'rect':
            self.rectangle(Vector((d[1], d[2])), *d[3:])

        else:
            raise ValueError("Unknown level delta type: " + repr(kind))

    def render(self, window: pyglet.window.Window):
        sw = self.manager.camera_transform(window, 35 / 2, 35 / 2)
        xd = self.manager.camera_transform_delta(window, 35, 0)
        yd = self.manager.camera_transform_delta(window, 0, 35)
        circumscribed = 35 * CIRCUM_MUL * self.manager.camera_zoom

        for (x, y), tile in self.tiles.items():
            if tile:
                t = self.manager.tile_types[tile]

                if not t.post:
                    #wx, wy = self.manager.camera_transform(window, x * 35 + 35 / 2, y * 35 + 35 / 2)
                    wx, wy = sw + xd * x + yd * y

                    if wx > -circumscribed and wx < window.width + circumscribed * 2 and wy > -circumscribed and wy < window.height + circumscribed * 2:
                        t.render(window, self, x, y, wx, wy, self.manager.camera_angle, self.manager.camera_zoom)
                        self.last_rendered.add((x, y))

                    elif (x, y) in self.last_rendered:
                        t.unrender(window, self, x, y, wx, wy, self.manager.camera_angle, self.manager.camera_zoom)

        self.batch.draw()

    def post_render(self, window: pyglet.window.Window):
        sw = self.manager.camera_transform(window, 35 / 2, 35 / 2)
        xd = self.manager.camera_transform_delta(window, 35, 0)
        yd = self.manager.camera_transform_delta(window, 0, 35)
        circumscribed = 35 * CIRCUM_MUL * self.manager.camera_zoom

        for (x, y), tile in self.tiles.items():
            if tile:
                t = self.manager.tile_types[tile]

                if t.post:
                    #x, wy = self.manager.camera_transform(window, x * 35 + 35 / 2, y * 35 + 35 / 2)
                    wx, wy = sw + xd * x + yd * y

                    if wx > -circumscribed and wx < window.width + circumscribed and wy > -circumscribed and wy < window.height + circumscribed:
                        t.post_render(window, self, x, y, wx, wy, self.manager.camera_angle, self.manager.camera_zoom)
                        self.last_rendered.add((x, y))

                    elif (x, y) in self.last_rendered:
                        t.post_unrender(window, self, x, y, wx, wy, self.manager.camera_angle, self.manager.camera_zoom)

        self.post_batch.draw()

    def __del__(self):
        for (x, y), tile in self.tiles.items():
            self.manager.tile_types[tile].unset(self, x, y)

        del self.tiles


class Manager(EntityContainer):
    def __init__(self, game, window):
        EntityContainer.__init__(self)

        self.game = game # type; yodine.game.Game
        self.window = window # type: pyglet.window.Window
        #self.entity_list = []
        #self.entity_index = {}

        self.systems = [] # type: List[System]
        self.event_listeners = {} # type: Dict[str, Callable]
        self.templates = {}
        self.tile_types = {} # type: Dict[str, TileType]
        self.component_types = component_types
        self.camera = Vector((0, 0))
        self.levels = {} # type: Dict[str, Level]
        self.default_level = self.create_level('_DEFAULT')
        self.current_level = self.default_level # type: Level
        self.loader = ModLoader()
        self.global_event_listeners = set()
        self.camera_angle = 0
        self.camera_zoom = 1.2
        self.dtime = None

        self.set_middle()

    def __contains__(self, eid: str) -> bool:
        if eid in self.entity_id_set:
            return True

        if self.current_level and eid in self.current_level.entity_id_set:
            return True

        return False

    def update(self, other_manager: 'Manager'):
        for e in self:
            loaded = e.id not in other_manager.entity_ids
            e.copy_transfer(other_manager)

            if loaded:
                other_manager.emit(e, 'loaded')

    def register_delta(self, delta_name, *args):
        if self.game.server:
            na = []

            for d in self.game.server.change_accum:
                dn2 = d[0]

                if delta_name == dn2:
                    if args == d[1:]:
                        continue

                    elif delta_name == 'set':
                        eid1, cname1, cval1 = d[1:]
                        eid2, cname2, cval2 = args
                        
                        if eid1 == eid2 and cname1 == cname2:
                            continue

                na.append(d)

            na.append((delta_name, *args))

            del self.game.server.change_accum
            self.game.server.change_accum = na
    
    def set_middle(self, size_x = None, size_y = None):
        if (size_x and size_y) or self.window:
            self.middle = Vector(((size_x or self.window.width) / 2, (size_y or self.window.height) / 2))

        else:
            self.middle = Vector((0, 0))

    def find_entity(self, eid):
        if eid in self.entity_ids:
            return Entity(self, eid)

        elif eid in self.current_level.entity_ids:
            return Entity(self.current_level, eid)

        raise ValueError("Entity not found: {}".format(eid))

    def camera_transform(self, window, x, y):
        v = Vector((x - self.camera.x, y - self.camera.y)).rotate(-self.camera_angle)

        v.x = v.x * self.camera_zoom + self.middle.x
        v.y = v.y * self.camera_zoom + self.middle.y

        return v

    def camera_transform_delta(self, window, x, y):
        return Vector((x, y)).rotate(-self.camera_angle) * self.camera_zoom

    def force_render_tile(self, window: pyglet.window.Window, tiletype: str, wx, wy):
        self.tile_types[tiletype].force_render_tile(self.current_level, window, wx, wy)

    def un_camera_transform(self, window, x, y):
        v = Vector((x - self.middle.x, y - self.middle.y)).rotate(self.camera_angle)

        v.x = v.x / self.camera_zoom + self.camera.x
        v.y = v.y / self.camera_zoom + self.camera.y

        return v

    def __iter__(self) -> Iterator['Entity']:
        for e in self.get_entities():
            yield e

        if self.current_level is not None:
            for e in self.current_level.get_entities():
                yield e

    def all_entity_ids(self) -> Iterator['str']:
        for eid in self.entity_id_set:
            yield eid

        if self.current_level is not None:
            for eid in self.current_level.entity_id_set:
                yield eid

    def change_level(self, lid: str):
        self.current_level = self.levels[lid]
        self.register_delta('clv', lid)

    def add_level_save(self, lid: str, save) -> Level:
        l = Level(lid, self)
        l.load_save(save)

        return self.add_level(l)

    def add_level(self, level: Level) -> Level:
        self.levels[level.id] = level

        if level.id != '_DEFAULT':
            self.register_delta('nlv', level.id, level.get_save())
            
        return level

    def create_level(self, lid: str) -> Level:
        return self.add_level(Level(lid, self))

    def add_tile_type(self, tt: TileType):
        self.tile_types[tt.name] = tt

    def move_camera(self, x=0, y=0, angle=0):
        self.camera += Vector((x, y))
        self.camera_angle += angle

    def set_camera(self, x=None, y=None, angle=None, zoom=None):
        if x is not None:
            self.camera.x = x

        if y is not None:
            self.camera.y = y

        if angle is not None:
            self.camera_angle = angle

        if zoom is not None:
            self.camera_zoom = zoom

    def load_mod(self, plugin_name: str):
        self.loader.load_one(plugin_name)

        for r in self.loader.routines['preload.' + plugin_name]:
            r(self.game)

        self.loader.apply(self)

        for r in self.loader.routines['postload.' + plugin_name]:
            r(self.game)

    def apply_mod(self, plugin_name: str, func: Callable):
        self.loader.load(plugin_name, func)

        for r in self.loader.routines['preload.' + plugin_name]:
            r(self.game)

        self.loader.apply(self)

        for r in self.loader.routines['postload.' + plugin_name]:
            r(self.game)

    def load_all_mods(self):
        for plugin_name in self.loader.load_all():
            for r in self.loader.routines['preload.' + plugin_name]:
                r(self.game)

            self.loader.apply(self)

            for r in self.loader.routines['postload.' + plugin_name]:
                r(self.game)

    def register_template(self, template: Type['EntityTemplate']) -> Type['EntityTemplate']:
        self.templates[template.name] = template(self)
        return template

    def register_component(self, cotype: Type['Component']) -> Type['Component']:
        self.component_types[cotype.__name__] = cotype
        return cotype

    def tick(self, dtime: float):
        self.set_middle()
        self.dtime = dtime

        for e in self:
            for s in self.systems:
                if hasattr(s, 'tick'):
                    s._tick(e, dtime)

        for t in self.tile_types.values():
            t.tick(self, dtime)

    def render(self, window: pyglet.window.Window):
        window.clear()

        if self.current_level is not None:
            self.current_level.render(window)

        for e in self:
            for s in self.systems:
                if hasattr(s, 'render'):
                    s._render(e, window)

        if self.current_level is not None:
            self.current_level.post_render(window)

    def apply(self, window: pyglet.window.Window) -> pyglet.window.Window:
        @window.event
        def on_draw():
            self.render(window)

        return window

    def reset_systems(self):
        self.systems = []

    def add_system(self, s: Type['System']) -> None:
        self.systems.append(s(self))

    def iter_grouped_templates(self, template_group: str) -> Iterator[Type['EntityTemplate']]:
        for template in self.templates:
            a = template.group.split('.')
            b = template_group.split('.')

            a = a[:len(b)]

            if tuple(a) == tuple(b):
                yield template

    def listen(self, event_name):       
        check_name = '_'.join(event_name) if type(event_name) is tuple else event_name

        def _decorator(self, func):
            if check_name not in self.event_listeners:
                self.event_listeners[check_name] = set()
            
            self.event_listeners[check_name] |= {func}
            return func

        return _decorator

    def add_listener(self, event_name, func):
        if event_name not in self.event_listeners:
            self.event_listeners[event_name] = set()

        self.event_listeners[event_name] |= {func}

    def global_listener(self, func):
        self.global_event_listeners |= {func}

    def emit_local(self, source, event_name, local, *args, **kwargs):
        check_name = '_'.join(event_name) if type(event_name) is tuple else event_name

        if check_name in self.event_listeners:
            for func in self.event_listeners[event_name]:
                func(source, *args)

        event_ctx = EventContext(event_name, self, source, local, **kwargs)

        for system in self.systems:
            system._on(check_name, event_ctx, *args)

        for tt in self.tile_types.values():
            tt._on(check_name, event_ctx, *args)

        for gel in self.global_event_listeners:
            gel(event_ctx, event_name, *args)

    def emit_all_local(self, event_name, local, *args, **kwargs):
        for e in self:
            self.emit_local(e, event_name, local, *args, **kwargs)

    def emit(self, source, event_name, *args, **kwargs):
        self.emit_local(source, event_name, self.game.id, *args, **kwargs)

    def emit_all(self, event_name, *args, **kwargs):
        self.emit_all_local(event_name, self.game.id, *args, **kwargs)

    def __getitem__(self, entity_id: str) -> 'Entity':
        return self.find_entity(entity_id)


component_types = {}

def register_component(cotype):
    component_types[cotype.__name__] = cotype
    return cotype


@register_component
class Component(object):
    def __init__(self, entity: 'Entity', name: str, value: Any = None):
        self.entity = entity
        self.name = name
        self._value = value

        self.component_init(value)

    def component_init(self, value: Any):
        pass
    
    def force_set(self, value: Any = None) -> bool:
        if self._value == value:
            return False

        self._value = value
        return True

    def set(self, value: Any = None):
        if self.force_set(value):
            self.entity.manager.register_delta('set', self.entity.id, self.name, value)
            self.entity.manager.emit(self.entity, ('change', self.name), self)

    def __repr__(self):
        return '[{} {} = {}]'.format(type(self).__name__, self.name, repr(self.value))

    @property
    def value(self):
        return self.get()

    @value.setter
    def value(self, val):
        self.set(val)

    def get(self):
        return self._value

    def json_get(self):
        return self._value


@register_component
class VectorComponent(Component):
    def component_init(self, value: Any):
        self._vec = Vector(self._value)

    def force_set(self, value: Any = None):
        self._value = list(value)
        self._vec.x, self._vec.y = self._value

        return True

    def get(self):
        return self._vec

    def json_get(self):
        return list(self._vec)


class Entity(object):
    def __init__(self, level: 'EntityContainer', identifier = None):
        self.level = level
        self.manager = getattr(level, 'manager', level)
        self.id = identifier or str(uuid.uuid4())

        self.level.entity_component_index.setdefault(self.id, {})

        if self.id not in self.level.entity_id_set:
            self.level.entity_ids.append(self.id)
            self.level.entity_id_set.add(self.id)
            self.level.entity_count += 1

    def transfer(self, new_level: EntityContainer):
        if self.id in new_level.entity_id_set or new_level is self.level:
            #raise RuntimeError("Tried to transfer an entity to a container it is already at!")
            return

        self.remove()
        self.copy_transfer(new_level)

        self.manager.register_delta('tsf', self.id, new_level.id)

    def copy_transfer(self, new_level: EntityContainer):
        comps = list(self.get_components()) # type: List[Component]
        
        new_level.entity_component_index[self.id] = {}

        if self.id not in new_level.entity_id_set:
            new_level.entity_ids.append(self.id)
            new_level.entity_id_set.add(self.id)
            new_level.entity_count += 1
        
        for cmpnt in comps:
            new_level.entity_component_index[self.id][cmpnt.name] = cmpnt

    def get_components(self) -> Iterator['Component']:
        return self.level.entity_component_index[self.id].values()

    def __hash__(self):
        return hash(self.id)

    def remove(self):
        del self.level.entity_component_index[self.id]
        self.level.entity_id_set.remove(self.id)
        self.level.entity_ids.remove(self.id)
        self.level.entity_count -= 1

        self.manager.register_delta('dsp', self.id)

    def create_component(self, name: str, value = None, kind = None) -> 'Component':
        ct = self.level.get_component_types()

        if kind is None:
            kind = Component

        elif kind in ct:
            kind = ct[kind]

        elif isinstance(kind, str):
            raise ValueError("Unknown component type: " + repr(kind))

        elif not (isinstance(kind, type) and issubclass(kind, Component)):
            raise TypeError("Bad component type (expected str or Type[Component] or None): " + repr(kind))

        comp = kind(self, name, value)
        self.level.entity_component_index[self.id][name] = comp

        self.manager.register_delta('mkc', self.id, name, value, kind.__name__)

        return comp

    def __iter__(self):
        return iter(self.get_components())

    def __getitem__(self, comp_name: str) -> 'Component':
        return self.level.entity_component_index[self.id][comp_name]

    def __setitem__(self, comp_name: str, value: Optional[Any] = None):
        if comp_name in self:
            c = self[comp_name]
            c.value = value

        else:
            self.create_component(comp_name, value)

    def __contains__(self, comp_name: str) -> bool:
        return comp_name in self.level.entity_component_index[self.id]

    def __delitem__(self, comp_name: str):
        if comp_name not in self:
            return

        del self.level.entity_component_index[self.id][comp_name]

        if comp_name != 'localplayer':
            self.manager.emit(self, 'component_remove', comp_name)

        self.manager.register_delta('del', self.id, comp_name)

    def has(self, *comp_names: Iterable[str]) -> bool:
        return all(cn in self for cn in comp_names)

    def has_any(self, *comp_names: Iterable[str]) -> bool:
        return any(cn in self for cn in comp_names)

    def __repr__(self):
        return '<[ {} {} ]>'.format(self.id, ', '.join(repr(c) for c in self.get_components()))


class System(object):
    listeners = []
    component_types = []
    component_checks = {}
    component_defaults = {}

    def component_check(self, func):
        def _inner(ctx: Union[EventContext, Entity], *args):
            source = getattr(ctx, 'source', ctx)

            if not self.component_types:
                return func(source, *args)

            else:
                components = {}

                for cotype, cocheck in self.component_checks.items():
                    if cotype not in source or source[cotype].value != cocheck:
                        return False

                for cotype in self.component_types:
                    if cotype in source:
                        components[cotype] = source[cotype]

                    else:
                        return False

                for cotype, codefault in self.component_defaults.items():
                    if cotype not in source:
                        source[cotype] = codefault

                    components[cotype] = source[cotype]

                func(ctx, *args, **components)
                return True

        return _inner

    def __init__(self, manager: Manager):
        self.manager = manager
        self.game = manager.game
        
        self.listeners = type(self).listeners
        self.component_types = type(self).component_types
        self.component_checks = type(self).component_checks
        self.component_defaults = type(self).component_defaults

        for event_name, func in self.listeners:
            manager.init_event(event_name)
            manager.add_listener(event_name, func)

        self.system_init()

    def system_init(self):
        pass
    
    def _tick(self, entity: Entity, *args) -> None:
        self.component_check(self.tick)(entity, *args)

    def _render(self, entity: Entity, window: pyglet.window.Window, *args) -> None:
        self.component_check(self.render)(entity, window, *args)

    def _on(self, event_name: str, event: EventContext, *args):
        if hasattr(self, 'on_' + event_name):
            return self.component_check(getattr(self, 'on_' + event_name))(event, *args)

    #def tick(self, entity: Entity, *args, **kwargs) -> None:
    #    pass

    #def render(self, entity: Entity, window: pyglet.window.Window, *args, **kwargs) -> None:
    #    pass


class SystemRegistry(object):
    def __init__(self):
        self.system_types = []

    def define(self, sys: Type[System]) -> Type[System]:
        self.system_types.append(sys)

        return sys

    def apply(self, manager: Manager) -> None:
        for st in self.system_types:
            manager.add_system(st)


class EntityTemplate(object):
    name = None # type: str
    group = None # type: Optional[str]
    default_components = [] # type: Iterable[Tuple[str, Any]]

    def __init__(self, manager: Manager):
        self.manager = manager
        self.default_component_index = {
            v[0]: (v[1] if len(v) > 1 else None) for v in self.default_components
        }

    def get_value(self, cname):
        return self.default_component_index[cname]

    def spawn(self, level: Level, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> Entity:
        components = list(components)
        has_components = set(c[0] for c in components)
        
        for dc in self.default_components:
            if dc[0] not in has_components:
                components.append(dc)

        return level.create_entity(components, identifier)



all_systems = SystemRegistry()
