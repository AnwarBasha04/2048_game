import random
import tkinter as tk
from tkinter import messagebox

class Game2048:
    def __init__(self, grid_size):
        self.n = grid_size
        self.mat = []
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.game_over = False

        self.grid = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                label = tk.Label(self.window, text="", font=("Helvetica", 24), width=4, height=2, borderwidth=2, relief="solid")
                label.grid(row=i, column=j, padx=5, pady=5)
                row.append(label)
            self.grid.append(row)

        self.start_game()
        self.window.bind("<Key>", self.key_pressed)
        self.window.mainloop()

    def add_new(self):
        a = random.randint(0, self.n-1)
        b = random.randint(0, self.n-1)
        while self.mat[a][b] != 0:
            a = random.randint(0, self.n-1)
            b = random.randint(0, self.n-1)
        self.mat[a][b] = 2

    def start_game(self):
        self.mat = [[0]*self.n for _ in range(self.n)]
        for _ in range(2):
            self.add_new()
        self.update_grid()

    def compress(self):
        new_mat = [[0]*self.n for _ in range(self.n)]
        for i in range(self.n):
            pos = 0
            for j in range(self.n):
                if self.mat[i][j] != 0:
                    new_mat[i][pos] = self.mat[i][j]
                    pos += 1
        self.mat = new_mat

    def merge(self):
        for i in range(self.n):
            for j in range(self.n-1):
                if self.mat[i][j] == self.mat[i][j+1] and self.mat[i][j] != 0:
                    self.mat[i][j] *= 2
                    self.mat[i][j+1] = 0

    def reverse(self):
        for i in range(self.n):
            self.mat[i].reverse()

    def transpose(self):
        self.mat = [list(row) for row in zip(*self.mat)]

    def move_left(self):
        self.compress()
        self.merge()
        self.compress()

    def move_right(self):
        self.reverse()
        self.move_left()
        self.reverse()

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    def check_status(self):
        if any(2048 in row for row in self.mat):
            return 1
        if any(0 in row for row in self.mat):
            return 0
        for i in range(self.n):
            for j in range(self.n-1):
                if self.mat[i][j] == self.mat[i][j+1]:
                    return 0
                if self.mat[j][i] == self.mat[j+1][i]:
                    return 0
        return 2

    def update_grid(self):
        for i in range(self.n):
            for j in range(self.n):
                value = self.mat[i][j]
                if value == 0:
                    self.grid[i][j].config(text="", bg="lightgray")
                else:
                    self.grid[i][j].config(text=str(value), bg=self.get_color(value), fg="green")

    def get_color(self, value):
        colors = {
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#cdc1b4")

    def key_pressed(self, event):
        if self.game_over:
            return

        key = event.keysym
        if key == 'Up':
            self.move_up()
        elif key == 'Down':
            self.move_down()
        elif key == 'Left':
            self.move_left()
        elif key == 'Right':
            self.move_right()

        self.update_grid()
        status = self.check_status()
        if status == 0:
            self.add_new()
            self.update_grid()
        elif status == 1:
            self.update_grid()
            messagebox.showinfo("2048", "You have won the game!")
            self.game_over = True
        elif status == 2:
            self.update_grid()
            messagebox.showinfo("2048", "You lost the game.")
            self.game_over = True

if __name__ == "__main__":
    grid_size = int(input("Choose the number of grids you want to play on: "))
    Game2048(grid_size)
