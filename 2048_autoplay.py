import matrix as mk
import strategy as stg

def autoplay(matrix, strategy):
    while True:
        direction = strategy(matrix.matrix.copy())
        matrix.update(direction)
        matrix.print()
        if matrix.gameover():
            print('matrix:')
            matrix.print()
            break


if __name__ == '__main__':
    print("----------------------------------")
    print('Welcome to 2048!')
    print('Author: Coconutboi')
    print('Version: 0.1')
    print('mode: autoplay')
    print('----------------------------------')
    print()
    matrix = mk.matrix(4)
    autoplay(matrix, stg.strategy)

    
    

    
