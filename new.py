import tkinter as tk

class Restart(tk.Button):
    def __init__(self, parent, board):
        self.parent = parent
        self = tk.Button.__init__(self, parent, text="O", font=("Arial", 12),
                                  command=lambda: board.reset())

class Custom(tk.Button):
    def __init__(self, parent, board, text, rows, cols, mines):
        self.parent = parent
        self = tk.Button.__init__(self, parent, text=text, font=("Arial", 12),
                                  command=lambda i=rows, j=cols, m=mines: board.change_size(i, j, m))
