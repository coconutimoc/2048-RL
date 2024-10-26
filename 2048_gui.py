from kernal import game2048
import tkinter as tk
import json
from datetime import datetime

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    for dict in config:
        if dict['task'] == "gui":
            config = dict
            break


class GUI:
    def __init__(self, master):
        #config the window
        self.master = master
        self.master.title(config["window"]["title"])
        self.master.geometry(config["window"]["geometry"])
        self.master.bind('<Key>', self.key_pressed)
        self.master.config(bg=config["window"]["bg"])

        #initialize the game
        self.game = game2048(dimension=config['dimension'])
        
        #initialize the UI
        self.score_label = tk.Label(self.master, text=f'Score:{self.game.score}', font=(config["cell"]["font"]["family"], config["cell"]["font"]["size"],\
                 config["cell"]["font"]["weight"])).grid(row=0, column=0, columnspan=self.game.dimension)
        self.cells = []
        for line in range(0, self.game.dimension):
            for column in range(0, self.game.dimension):
                cell = tk.Label(self.master, text='', font=(config["cell"]["font"]["family"], config["cell"]["font"]["size"],\
                 config["cell"]["font"]["weight"]), width=config["cell"]["width"], height=config["cell"]["width"], bg=config["cell"]["color"]["0"])
                cell.grid(row=line+1, column=column)
                self.cells.append(cell)
        self.update_ui()

    def update_ui(self):
        for i in range(0, self.game.dimension):
            for j in range(0, self.game.dimension):
                index = i * self.game.dimension + j
                value = self.game.matrix[i][j]
                if value == 0:
                    self.cells[index].config(text='', bg='gray')
                else:
                    self.cells[index].config(text=str(int(value)), bg=config["cell"]['colors'][str(value)])
        self.score_label.config(text=f'Score:{self.game.score}')
    
    def key_pressed(self, event):
        if config["key"][event.keysym] in ['up', 'down', 'left', 'right']:
            self.game.update(config["key"][event.keysym])
            self.update_ui()
            if self.game.gameover():
                self.game_over()
        if config["key"][event.keysym] == 'quit':
            self.master.quit()
    
    def game_over(self):
        self.game_over_label = tk.Label(self.master, text='Game Over!', font=('Arial', 40, 'bold'), bg='red')
        self.game_over_label.grid(row=0, column=0, columnspan=self.game.dimension)
        self.master.unbind('<Key>')
        self.master.bind('<Key>', self.quit)
        with open('log.csv', 'a+') as log:
            log.write(f'{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, config["username"], {self.game.dimension},{self.game.score}\n')
        
    def quit(self, event):
        if config["key"][event.keysym] == 'quit':
            self.master.quit()

if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
    
