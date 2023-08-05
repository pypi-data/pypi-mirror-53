import sys, functools
import os

from . import game



def main():
    this_game = game.Game(os.environ.get('YODINE_GAME', 'yodine_data'), sys.argv[1] if len(sys.argv) > 1 else 'main.save.json')
    print('Starting...')
    this_game.run()