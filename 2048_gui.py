"""
This file creates a GUI for the 2048 game.
Configurations of GUI are stored in gui_config.py.
"""

from kernal import game2048
import tkinter as tk
from datetime import datetime
from config.gui_config import *

class GUI:
    def __init__(self, master):
        # Config the window
        self.master = master
        self.master.title(window_title)
        self.master.geometry(f"{dimension*75+50}x{dimension*75+50}")
        self.master.bind('<Key>', self.key_pressed)
        self.master.config(bg=window_bg)

        # Create a frame to center the content
        self.frame = tk.Frame(self.master, bg=window_bg)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Initialize the game
        self.game = game2048(dimension=dimension)
        
        # Initialize the UI
        self.score_label = tk.Label(self.frame, text=f'Score:{int(self.game.score)}', font=(cell_font_family, cell_font_size, cell_font_weight))
        self.score_label.grid(row=0, column=0, columnspan=self.game.dimension, pady=10)
        
        self.cells = []
        for line in range(0, self.game.dimension):
            for column in range(0, self.game.dimension):
                cell = tk.Label(self.frame, text='', font=(cell_font_family,cell_font_size, cell_font_weight), width=cell_width, height=cell_height, bg=colormap["0"])
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
                    self.cells[index].config(text=str(int(value)), bg=colormap[str(int(value))])
        self.score_label.config(text=f'Score:{int(self.game.score)}')
    
    def key_pressed(self, event):
        """
        Handle the key pressed event
        """
        if keymap[event.keysym] in ['up', 'down', 'left', 'right']:
            self.game.update(keymap[event.keysym])
            self.update_ui()
            if self.game.gameover():
                self.game_over()
        if keymap[event.keysym] == 'quit':
            self.master.destroy()
    
    def game_over(self):
        self.game_over_label = tk.Label(self.master, text='Game Over!', font=('Arial', 40, 'bold'), bg='red')
        self.game_over_label.grid(row=0, column=0, columnspan=self.game.dimension)
        self.master.unbind('<Key>')
        self.master.bind('<Key>', self.quit)
        with open('log.csv', 'a+') as log:
            log.write(f'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {user}, {self.game.dimension},{self.game.score}\n')
        
    def quit(self, event):
        if keymap[event.keysym] == 'quit':
            self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
    
