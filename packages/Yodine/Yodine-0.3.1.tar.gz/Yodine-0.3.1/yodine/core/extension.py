from typing import List, Type, Callable, Optional, Any, Iterator

import os
import sys
import importlib
import warnings
import pkg_resources



class PluginNotFoundError(ImportError):
    pass


class UnmetPluginDependenciesError(PluginNotFoundError):
    pass


class RoutineSet(object):
    def __init__(self, loader: 'ModLoader'):
        self.__loader = loader

    def __getattr__(self, name):
        if name == '__loader':
            return self.__loader

        try:
            return self.__loader._routines[name]

        except KeyError:
            raise LookupError("No such routine '{}' registered in this loader!".format(name))

    def __getitem__(self, group: str) -> Iterator[Callable]:
        for r in self:
            if r.GROUP:
                a = r.GROUP.split('.')
                b = group.split('.')

                a = a[:len(b)]

                if tuple(a) == tuple(b):
                    yield r

    def __iter__(self) -> Iterator[Callable]:
        return iter(self.__loader._routines.values())


class ModLoader(object):
    def __init__(self):
        self._routines = {} # type: Dict[str, Callable]
        self.templates = [] # type: List[Type['EntityTemplate']]
        self.systems = [] # type: List[Type['System']]
        self.component_types = [] # type: List[Type['Component']]
        self.tile_types = [] # type: List['TileType']
        self.loaded = set()
        self.routines = RoutineSet(self)

    def load(self, name: str, module_loaded: Callable) -> Any:
        if name in self.loaded:
            return

        self.loaded.add(name)
        return module_loaded(self)

    def load_all(self):        
        for ep in pkg_resources.iter_entry_points('yodine.plugin'):
            self.load(ep.name, ep.load())
            yield ep.name

    def load_one(self, name: str) -> Any:
        for ep in pkg_resources.iter_entry_points('yodine.plugin', name):
            return self.load(ep.name, ep.load())

    def apply(self, manager: 'Manager'):
        for s in self.systems:
            manager.add_system(s)

        for t in self.templates:
            manager.register_template(t)

        for ct in self.component_types:
            manager.register_component(ct)

        for tt in self.tile_types:
            manager.add_tile_type(tt)

        self.templates = [] # type: List[Type['EntityTemplate']]
        self.systems = [] # type: List[Type['System']]
        self.component_types = [] # type: List[Type['Component']]
        self.tile_types = [] # type: List['TileType']

    def system_type(self, systype: Type['System']) -> Type['System']:
        self.systems.append(systype)
        return systype

    def add_tile_type(self, tiletype: 'TileType') -> 'TileType':
        self.tile_types.append(tiletype)
        return tiletype

    def routine(self, group: Optional[str] = None, name: Optional[str] = None) -> Callable:
        def _decorator(function: Callable) -> Callable:
            function.NAME = name
            function.GROUP = group

            self._routines[name or function.__name__] = function
            return function

        return _decorator

    def template(self, template: Type['EntityTemplate']) -> Type['EntityTemplate']:
        self.templates.append(template)
        return template

    def component_type(self, component_type: Type['Component']) -> Type['Component']:
        self.component_types.append(component_type)
        return component_type