import tkinter as tk
import random
import matrix as mk
import math
import csv
import time

class Game2048:
    def __init__(self, master, dimension=4):
        self.master = master
        self.master.title('2048 Game')
        self.master.geometry('600x600')
        self.master.resizable(0, 0)
        self.grid_size = dimension
        self.cell_size = 600 // self.grid_size
        self.cells = []
        self.matrix = mk.matrix(self.grid_size)
        self.init_grid()
        self.master.bind("<Key>", self.key_handler)

    def init_grid(self):
        background = tk.Frame(self.master, bg='azure3', width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size)
        background.grid(pady=(100, 0))
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell = tk.Frame(background, bg='azure4', width=self.cell_size, height=self.cell_size)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(master=cell, text='', bg='azure4', justify=tk.CENTER, font=('arial', 22, 'bold'), width=4, height=2)
                t.grid()
                row.append(t)
            self.cells.append(row)
        self.update_grid()  

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.matrix.matrix[i][j]
                if value == 0:
                    self.cells[i][j].configure(text='', bg='azure4')
                else:
                    color = "#{:02x}{:02x}{:02x}".format(255 - int(math.log(value, 2) * 30), 255 - int(math.log(value, 2) * 30), 255)
                    self.cells[i][j].configure(text=str(int(value)), bg=color)

    def key_handler(self, event):
        key = event.keysym
        if key in ('Up', 'Down', 'Left', 'Right'):
            self.matrix.update(key.lower())
            self.update_grid()
            if self.matrix.gameover():
                self.game_over()
        if key == '<ctrl-q>':
            self.master.quit()
            print('Successfully quit! No score will be recorded.')

    def game_over(self):
        game_over_frame = tk.Frame(self.master, borderwidth=2)
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(game_over_frame, text="Game Over!", bg='red', fg='white', font=('arial', 22, 'bold')).pack()
        print('Game Over! Your score is:', self.matrix.score)
        if globals().get('username') is not None:
                with open('.dict/log.csv', 'a') as log:
                    writer = csv.writer(log)
                    writer.writerow([username, self.matrix.score, self.matrix.maxnum,self.matrix.dimension,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())])

if __name__ == "__main__":
    print("----------------------------------")
    print('Welcome to 2048!')
    print('Author: Coconutboi')
    print('Version: 0.1')
    print('mode: GUI')
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

    root = tk.Tk()
    game = Game2048(root,dimension)
    root.mainloop()