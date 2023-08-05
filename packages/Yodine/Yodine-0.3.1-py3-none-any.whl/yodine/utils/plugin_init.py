import sys
import os


default_module = """
# ============== {name} ==============
#             by {author}
# licensed under {license}
#
#   {description}

# This is the main code of your plugin.
# Here you will add all of the logic that will
# be used by your plugin.

# The lines below import all of the classes you'll
# use from Yodine.
from yodine.core.entity import EntityTemplate, System, TileType
from yodine.core.extension import ModLoader
from yodine.core.vector import ComponentVector

# Other general imports below.
import pyglet
import os



# Defines an extra resource path.
pyglet.resource.path.append(os.path.join(os.path.split(__file__)[0], 'assets'))
pyglet.resource.reindex()


# These helper functions will access assets for you :)
def asset_path(asset_name: str) -> str:
    return os.path.join(os.path.split(__file__)[0], 'assets', asset_name)

def open_asset(asset_name: str) -> file:
    return open(asset_path(asset_name))


# This function will be called when the plugin is
# loaded.
def loaded(loader: ModLoader):
    # Defines a standard tile type (background - does nothing).
    class FloorTileType(TileType):
        name = 'floor'

    loader.add_tile_type(FloorTileType(pyglet.resource.image(asset_path('tiles/floor.png'))))

    # Defines a custom tile type (foreground - e.g. collides).
    class WallTileType(TileType):
        name = 'wall'

        def on_move(self, manager, entity, start_pos):
            if self.is_inside(manager, entity):
                ComponentVector(entity['position']) << start_pos

    loader.add_tile_type(WallTileType(pyglet.resource.image(asset_path('tiles/wall.png'))))
    
    # Defines a routine, which may be used by this or other
    # plugins.
    @loader.routine()
    def moo():
        # This can later be accessed via loader.routine (see
        # MooSystem).
        with open_asset('moo.txt') as moofile:
            print(moofile.read().strip())

    # Defines a game initialization routine, by giving the routine decorator a group string.
    @loader.routine('yodine.init')
    def begin():
        print("Welcome to the Moo Moo Mountains!")

    # Defines a system to be registered by
    # the loader.
    @loader.system_type
    class MyPluginSystem(System):
        # This is a list of components that the entity MUST
        # have, and that will be passed to tick, render, and
        # to event handlers (on_*).
        component_types = ['name']

        # This is a list of components that the entity MAY
        # have, and that will be passed to tick, render, and
        # to event handlers (on_*).
        # -----
        # If those components are not present, the default values
        # are passed instead.
        component_defaults = {{'postfix': "I'm a dumb plugin, teehee!"}}

        # This method of a system is called every tick, i.e., everytime
        # the game updates itself.
        # It is responsible for updating the entity.
        def tick(self, entity: Entity, *args, **kwargs) -> None:
            print("TICK!")

        # This method of a system is called every time the game is rendered.
        # It is responsible for rendering the entity.
        def render(self, entity: Entity, window: pyglet.window.Window, name, postfix, *args, **kwargs) -> None:
            print("I will print {{}}... already did! {{}}".format(name, postfix))
    
    @loader.system_type
    class MooSystem(System):
        # Components that must have certain values
        # in order for this system to operate on
        # a certain entity. Note that 'operate' includes
        # `tick`, `render` and `on_*` system methods.
        component_checks = {{'moo': 'YES!'}}

        def render(self, entity: Entity, *args, **kwargs) -> None:
            # Grabs a routine and calls it.
            loader.routines.moo()
            
            # This is our moo() routine defined earlier!
            # How magic is that? :)

    # Defines an entity template, a way to specify how certian
    # entities should be created.
    @loader.template
    class MyPluginEntityType(EntityTemplate):
        # The name of this template. Used when looking it up.
        name = 'Cow'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'living.passive'

        # A list of default components.
        default_components = [
            ('name', 'a cow'),
            ('postfix', 'MOOO!'),
            ('moo', 'YES!')
        ]


""".lstrip()

setup_template = """
from setuptools import setup
from {name}.version import VERSION_STR as VERSION

import os



NAME = '{name}'
DESCRIPTION = '{description}'
AUTHOR = '{author}'
REQUIRES_PYTHON = '>=3.5.0'
LICENSE = '{license}'


# What packages are required for this plugin to work?
REQUIRED = [
    # Yodine plugin dependencies:
    'yodine_data',

    # General dependencies:
    # 'numpy'
]

with open('README.md') as readme:
    long_description = readme.read()
        

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    packages=['{name}'],

    entry_points={{
        'yodine.plugin': ['{{0}} = {{0}}.plugin:loaded'.format(NAME)],
    }},
    install_requires=REQUIRED,
    license=LICENSE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    package_data={{NAME: ['assets/*', 'assets/**/*']}},
    include_package_data=True,
)
""".lstrip()

gitignore = """
# === Python ===

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
fastenv/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Sphinx documentation
docs/_build/

# PyBuilder
target/

#Ipython Notebook
.ipynb_checkpoints

# pyenv
.python-version
""".lstrip()

readme_template = """
# {name}

**A Yodine plugin by {author}**

{description}

-----

Licensed under {license}.
""".lstrip()


def init_plugin(plugin_name, folder='.', author='an anonymous pluginwriter', description='', license='MIT'):
    plugin_pkg = os.path.join(folder, plugin_name)
    plugin_init = os.path.join(plugin_pkg, '__init__.py')
    plugin_code = os.path.join(plugin_pkg, 'plugin.py')
    asset_folder = os.path.join(plugin_pkg, 'assets')
    setup_py = os.path.join(folder, 'setup.py')
    setup_cfg = os.path.join(folder, 'setup.cfg')
    readme = os.path.join(folder, 'README.md')
    manifest = os.path.join(folder, 'MANIFEST.in')
    gitignore_path = os.path.join(folder, '.gitignore')
    version = os.path.join(plugin_pkg, 'version.py')

    if not os.path.exists(plugin_pkg):
        os.makedirs(plugin_pkg)

    if not os.path.exists(plugin_code):
        open(plugin_code, 'w').write(default_module.format(name=plugin_name, author=author, description=description, license=license))

    if not os.path.exists(plugin_init):
        open(plugin_init, 'w')

    if not os.path.exists(asset_folder):
        os.makedirs(asset_folder)

    if not os.path.exists(setup_py):
        open(setup_py, 'w').write(setup_template.format(name=plugin_name, author=author.replace('\'', '\\\''), description=description.replace('\'', '\\\''), license=license.replace('\'', '\\\'')))

    if not os.path.exists(readme):
        open(readme, 'w').write(readme_template.format(name=plugin_name, author=author, description=description, license=license))

    if not os.path.exists(gitignore_path):
        open(gitignore_path, 'w').write(gitignore)

    if not os.path.exists(version):
        open(version, 'w').write('VERSION_TUPLE = (0, 1, 0)\nVERSION_POSTFIX = \'\'\n\nVERSION_STR = \'.\'.join(str(v) for v in VERSION_TUPLE) + VERSION_POSTFIX\n')


if __name__ == "__main__":
    print("What is the name of your brand new plugin?")
    plugin_name = input('> ')
    print("What is your author name? (can be your real name, a nickname, or even just your email!)")
    author = input('> ')
    print("Give your plugin a brief description.")
    description = input('> ')
    print("And a license! (default: MIT)")
    license = input('> ') or 'MIT'
    print("In which folder do you want to set this plugin project up? (default: {})".format(plugin_name))
    folder = input('> ') or plugin_name
    print()
    
    try:
        init_plugin(plugin_name, folder, author, description, license)

    except RuntimeError:
        print("Plugin already found (setup.py), aborting.")
        exit(1)

    else:
        print("Plugin project initialized!")
        exit(0)