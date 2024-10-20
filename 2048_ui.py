from matrix import matrix
import time
import csv


if __name__ == '__main__':
    print("----------------------------------")
    print('Welcome to 2048!')
    print('Author: Coconutboi')
    print('Version: 0.1')
    print('mode: UI')
    print('----------------------------------')
    print()


    with open('.dict/user.csv', 'a+') as user_file:
        users = csv.reader(user_file)
        writer = csv.writer(user_file)
        print('----------------------------------')
        if input ('Do you want to login?[y/n]: ') in ['y', 'Y']:
            while True:
                username = input('Username: ')
                if users is not None:
                    for user in users:
                        if user[0] == username:
                            correct_password = user[1]
                if globals().get('correct_password') is not None:
                    while True:
                        password = input('Password: ')
                        if password == correct_password:
                            print('Welcome back,', username)
                            break
                        else:
                            print('Password incorrect! Please try again.')
                            continue

                else:
                    if input('User not found! Do you want to create a new account?[y/n]:') in ['y', 'Y']:
                        while True:
                            username = input('Username: ')
                            password = input('Password: ')
                            if password == input('Confirm password: '):
                                writer.writerow([username, password])
                                print('Account created successfully!')
                                break
                            else:
                                print('Password not match! Please try again.')
                        break
                    else:
                        print('Please try again.')
                        continue
        else:
            print('Now you are playing as a guest.')
    print()
    dimension = int(input('Dimension: '))
    print()


    print('-----------------------------')
    print('Instructions:')
    print('"w" to move up')
    print('"s" to move down')
    print('"a" to move left')
    print('"d" to move right')
    print('"q" to quit')
    print('-----------------------------')
    print()


    direction_dict = {'w': 'up', 's': 'down', 'a': 'left', 'd': 'right'}
    game = matrix(dimension)
    while True:
        game.print()
        if game.gameover():
            print('Game Over! Your score is:', game.score)
            if globals().get('username') is not None:
                with open('.dict/log.csv', 'a') as log:
                    writer = csv.writer(log)
                    writer.writerow([username, game.score, game.maxnum, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())])
            break
        direction = input('Action: ')
        if direction == 'q':
            print('Successfully quit! No score will be recorded.')
            break
        game.update(direction_dict[direction])
        print('-------------------------')