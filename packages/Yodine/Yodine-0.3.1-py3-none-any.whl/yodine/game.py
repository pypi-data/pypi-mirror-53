import time
import uuid
import traceback
import random
import trio
import os
import pyglet
import random

from typing import Optional, Callable, Tuple
from .core.entity import Manager, Entity, Component
from .core.vector import Vector
from .core.network import Client, Server
from .core.advjson import json_adv_dump, json_adv_load
from . import gamedefs
from pyglet.gl import *
from pyglet import clock


# Credits: trio tutorial
class Tracer(trio.abc.Instrument):
    def before_run(self):
        print("!!! run started")

    def _print_with_task(self, msg, task):
        # repr(task) is perhaps more useful than task.name in general,
        # but in context of a tutorial the extra noise is unhelpful.
        print("{}: {}".format(msg, task.name))

    def task_spawned(self, task):
        self._print_with_task("### new task spawned", task)

    def task_scheduled(self, task):
        self._print_with_task("### task scheduled", task)

    def before_task_step(self, task):
        self._print_with_task(">>> about to run one step of task", task)

    def after_task_step(self, task):
        self._print_with_task("<<< task step finished", task)

    def task_exited(self, task):
        self._print_with_task("### task exited", task)

    def before_io_wait(self, timeout):
        if timeout:
            print("### waiting for I/O for up to {} seconds".format(timeout))
        else:
            print("### doing a quick check for I/O")
            
        self._sleep_time = trio.current_time()

    def after_io_wait(self, timeout):
        duration = trio.current_time() - self._sleep_time
        print("### finished I/O check (took {} seconds)".format(duration))

    def after_run(self):
        print("!!! run finished")


class EventLoop(object):
    def __init__(self, window):
        self.window = window
        self.stop()

    def run(self):
        trio.run(self.async_run)

    def stop(self):
        self.running = False

    async def async_run(self):
        if self.window:
            self.running = True

            while self.running:
                clock.tick()

                self.window.switch_to()
                self.window.dispatch_events()
                self.window.dispatch_event('on_draw')
                self.window.flip()

                await trio.sleep(0)

            self.window.close()


class Game(object):
    def __init__(self, game_name: str, database_file: Optional[str] = None, client_addr: str = None, server_port: int = None, dedicated: bool = False, player_name: str = None):
        self.dedicated = dedicated or os.environ.get('YODINE_DEDICATED', 'NO').upper() in ('YES', 'TRUE', 'Y')

        self.random = random.Random()
        self.random.seed(time.time())
        
        self.scheduled = []

        server_port = server_port or int(os.environ.get('YODINE_LISTEN', 0)) or None
        client_addr = client_addr or os.environ.get('YODINE_CONNECT', None)

        self.id = str(uuid.uuid4()) # used for network identification
        print("Local ID: ", self.id)

        if not self.dedicated:
            self.window = pyglet.window.Window(visible=False, resizable=True, caption='Yodine')

        else:
            self.window = None

        self.manager = Manager(self, self.window) # type: Manager
        self.database_file = database_file # type: Optional[str]
        self.player_name = player_name or os.environ.get('YODINE_NAME', 'Anon_' + str(random.randint(1, 1999)))

        gamedefs.load_game(game_name, self)
        self.event_loop = EventLoop(self.window)
        self.keyboard = None

        # Enable blending for alpha channel images
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # Multiplayer
        if client_addr:
            client_hostname, client_port = client_addr.split(':')
            self.client = Client(self, (client_hostname, int(client_port)))

        else:
            self.client = None

        if server_port:
            self.server = Server(self, server_port)

        else:
            self.server = None

        # Load the game.
        self.load(game_name)

    def stop(self):
        self.save()

        if self.window:
            self.window.close()
            self.window = None

        if self.event_loop:
            self.event_loop.stop()

        if self.server:
            self.server.stop()

        if self.client:
            self.client.stop()

    async def tick_scheduled(self, dt):
        sc = []

        for s in self.scheduled:
            evt, when, func, args, kwargs = s

            if when <= time.time():
                func(*args, **kwargs)

            else:
                sc.append(s)

        self.scheduled = sc

    async def loop_schedules(self):
        ot = time.time()

        while (self.client and self.client.running) or (self.server and self.server.running):
            t = time.time()
            dt = t - ot
            ot = t

            await self.tick_scheduled(dt)
            await trio.sleep(1 / 15)

    async def loop(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.event_loop.async_run)
            nursery.start_soon(self.loop_schedules)

            if self.server:
                nursery.start_soon(self.server.run)
                self.server.running = True

                if self.dedicated:
                    nursery.start_soon(self.dedicated_ticking)

            if self.client:
                nursery.start_soon(self.client.run)

    async def dedicated_ticking(self):
        ot = time.time()

        while self.server and self.server.running:
            t = time.time()
            dt = t - ot
            ot = t

            self.manager.tick(dt)

            await trio.sleep(1 / 30)

    def load(self, init: Callable):
        for e in self.manager:
            e.remove()

        self.manager.levels = {'_DEFAULT': self.manager.default_level}
        
        if self.database_file and os.path.exists(self.database_file) and not self.client:
            with open(self.database_file, 'r') as dbfp:
                data = json_adv_load(dbfp.read())

                for level in data['levels']:
                    level_obj = self.manager.add_level_save(level['id'], level)

                    for entity in level['entities']:
                        level_obj.load_entity(entity['components'], entity['id'])

                for entity in data['entities']:
                    self.manager.load_entity(entity['components'], entity['id'])

                self.manager.change_level(data['currlevel'])

            found = False

            if not self.dedicated and not self.client:
                for entity in self.manager:
                    if entity.has('name', 'player', 'localplayer'):
                        if entity['name'].value == self.player_name:
                            entity['localplayer'] = self.id # redefine localplayer
                            found = True

                if not found:
                    self.init_player()

            if not len(self.manager):
                gamedefs.init_game(self)

                if not self.dedicated and not self.client:
                    self.init_player()
                
                self.save()

            else:
                self.emit_all('loaded')
            
        else:
            gamedefs.init_game(self)

            if not self.dedicated and not self.client:
                self.init_player()

            self.save()

    def init_player(self):
        for r in self.manager.loader.routines['init.player']:
            r(self)

    def save(self):
        if self.database_file:
            self.emit_all('saved')

            with open(self.database_file, 'w') as dbfp:
                data = {
                    'levels': [
                        {
                            'id': l.id,
                            'entities': [
                                {
                                    'components': [(c.name, c.json_get(), type(c).__name__) for c in e],
                                    'id': e.id
                                }
                                for e in l.get_entities()
                            ],
                            'deltas': l.deltas
                        } for l in self.manager.levels.values()
                    ],
                    'entities': [
                        {
                            'components': [(c.name, c.json_get(), type(c).__name__) for c in e],
                            'id': e.id
                        }
                        for e in self.manager.get_entities()
                    ],
                    'currlevel': self.manager.current_level.id
                }

                dbfp.write(json_adv_dump(data))

    def on_draw(self):
        if not self.dedicated:
            self.manager.render(self.window)

    def on_mouse_drag(self, x, y, dx, dy, button, mod):
        self.emit_all(('mouse', 'drag'), self.window, Vector((x, y)), Vector((dx, dy)), button, mod)

    def on_mouse_motion(self, x, y, dx, dy):
        self.emit_all(('mouse', 'move'), self.window, Vector((x, y)), Vector((dx, dy)))

    def on_mouse_enter(self, x, y):
        self.emit_all(('mouse', 'enter'), self.window, Vector((x, y)))

    def on_mouse_leave(self, x, y):
        self.emit_all(('mouse', 'leave'), self.window, Vector((x, y)))

    def on_mouse_press(self, x, y, button, modifiers):
        self.emit_all(('mouse', 'press'), self.window, Vector((x, y)), button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.emit_all(('mouse', 'release'), self.window, Vector((x, y)), button, modifiers)

    def on_key_press(self, button, modifiers):
        self.emit_all(('key', 'press'), self.window, button, modifiers)

    def on_key_release(self, button, modifiers):
        self.emit_all(('key', 'release'), self.window, button, modifiers)

    def emit_all(self, event, *args, **kwargs):
        self.manager.emit_all(event, *args, **kwargs)

    def net_emit(self, source, event, *args, **kwargs):
        if self.client:
            self.client.emit(source, event, *args, **kwargs)
            self.scheduled.append((event, time.time() + self.client.average_latency, self.manager.emit, (source, event, *args), kwargs))

        else:
            self.manager.emit(source, event, *args, **kwargs)

    def server_net_emit(self, source, event, *args, **kwargs):
        if self.server:
            self.server.emit(source, event, *args, **kwargs)

    def net_emit_change(self, source, compname, compvalue):
        if self.client:
            self.client.send('change', source, compname, compvalue)

    def on_close(self):
        self.stop()

    def run(self):
        self.keyboard = pyglet.window.key.KeyStateHandler()

        if not self.dedicated:
            self.window.push_handlers(self.keyboard)
            self.window.push_handlers(self)

            def tick(dtime):
                # tick
                t = time.time()
                dt = t - self.last_time
                self.last_time = t

                self.manager.tick(dtime)

            clock.schedule_interval(tick, 1 / 40)

            self.window.set_visible()

        try:
            self.last_time = time.time()
            
            trio.run(self.loop)
            #trio.run(self.loop, instruments=[Tracer()])

        except KeyboardInterrupt:    
            self.stop()
            traceback.print_exc()