"""
Functions that manipulate a game played automatically with strategies.
"""
import glob,os,importlib.util,re,itertools
strategy_files = glob.glob('strategies/*.py')
for file in strategy_files:
    module_name = os.path.splitext(os.path.basename(file))[0]
    spec = importlib.util.spec_from_file_location(module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals()[module] = module

def game(gameboard,*args):
    """
    gameboard: the gameboard
    *args: (player, strategy)
    """
    log = []
    def autoplay():
        nonlocal log
        while True:
            for player,strategy in args:
                action = strategy(gameboard.matrix.copy())
                gameboard.update(action)
                log.append([gameboard.status(),player,action])
                if gameboard.gameover():
                    print('Game Over!')
                    gameboard.print()
                    return log
    return autoplay