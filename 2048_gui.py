"""
This file creates a GUI for the 2048 game.
Configurations of GUI are stored in config.json.
"""


from kernal import game2048
import tkinter as tk
import json
from datetime import datetime

#load the configurations from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    for dict in config:
        if dict['task'] == "gui":
            config = dict
            break


class GUI:
    def __init__(self, master):
                # Config the window
        self.master = master
        self.master.title(config["window"]["title"])
        self.master.geometry(f"{config['dimension']*75+50}x{config['dimension']*75+50}")
        self.master.bind('<Key>', self.key_pressed)
        self.master.config(bg=config["window"]["bg"])

        # Create a frame to center the content
        self.frame = tk.Frame(self.master, bg=config["window"]["bg"])
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Initialize the game
        self.game = game2048(dimension=config['dimension'])
        
        # Initialize the UI
        self.score_label = tk.Label(self.frame, text=f'Score:{int(self.game.score)}', font=(config["cell"]["font"]["family"], config["cell"]["font"]["size"], config["cell"]["font"]["weight"]))
        self.score_label.grid(row=0, column=0, columnspan=self.game.dimension, pady=10)
        
        self.cells = []
        for line in range(0, self.game.dimension):
            for column in range(0, self.game.dimension):
                cell = tk.Label(self.frame, text='', font=(config["cell"]["font"]["family"], config["cell"]["font"]["size"], config["cell"]["font"]["weight"]), width=config["cell"]["width"], height=config["cell"]["height"], bg=config["cell"]["color"]["0"])
                cell.grid(row=line+1, column=column, padx=5, pady=5, sticky='nsew')
                self.cells.append(cell)

        # Configure grid layout to expand
        for i in range(self.game.dimension + 1):
            self.frame.grid_rowconfigure(i, weight=1)
            self.frame.grid_columnconfigure(i, weight=1)

        self.update_ui()

    def update_ui(self):
        """
        Update the UI based on the game matrix
        """
        for i in range(0, self.game.dimension):
            for j in range(0, self.game.dimension):
                index = i * self.game.dimension + j
                value = self.game.matrix[i][j]
                if value == 0:
                    self.cells[index].config(text='', bg='gray')
                else:
                    self.cells[index].config(text=str(int(value)), bg=config["cell"]['color'][str(int(value))])
        self.score_label.config(text=f'Score:{int(self.game.score)}')
    
    def key_pressed(self, event):
        """
        Handle the key pressed event
        """
        if config["key"][event.keysym] in ['up', 'down', 'left', 'right']:
            self.game.update(config["key"][event.keysym])
            self.update_ui()
            if self.game.gameover():
                self.game_over()
        if config["key"][event.keysym] == 'quit':
            self.master.destroy()
    
    def game_over(self):
        self.game_over_label = tk.Label(self.master, text='Game Over!', font=('Arial', 40, 'bold'), bg='red')
        self.game_over_label.grid(row=0, column=0, columnspan=self.game.dimension)
        self.master.unbind('<Key>')
        self.master.bind('<Key>', self.quit)
        with open('log.csv', 'a+') as log:
            log.write(f'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {config["user"]}, {self.game.dimension},{self.game.score}\n')
        
    def quit(self, event):
        if config["key"][event.keysym] == 'quit':
            self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
    
