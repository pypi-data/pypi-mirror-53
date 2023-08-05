from .core.entity import Level, TileType
from .core.vector import Vector


# This function is responsible for
# loading the game.
def load_game(game_data: str, game):
    manag = game.manager
    manag.load_mod(game_data)

# This function is responsible for
# initializing the game.
def init_game(game):
    manag = game.manager

    for routine in manag.loader.routines['init.game']:
        routine(game)