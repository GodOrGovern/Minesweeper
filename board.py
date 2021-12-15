import tkinter as tk
from random import randint
from timer import Timer

colors = {0: "black", 1: "blue", 2: "green", 3: "red", 4: "purple",
          5: "maroon", 6: "turquoise",  7: "black", 8: "gray", 9: "black"}
default = {"text": "    ", "bg": "#c6c6c6", "relief": "raised", "bd": 1, "font": "Mono 11 bold"}
empty = {"relief": "sunken"}
number = {"relief": "sunken"}
flag = {"bg": "red"}

class Space(tk.Label):
    def __init__(self, board, row, col):
        tk.Label.__init__(self, board.parent, default)
        self.board = board
        self.row = row
        self.col = col
        self.value = 0
        self.revealed = False
        self.flagged = False
        self.init_label()

    def init_label(self):
        self.bind("<Button-1>", lambda e: self.on_left_click())
        self.bind("<Button-3>", lambda e: self.on_right_click())
        self.grid(row=self.row, column=self.col)

    def gen_adjacent(self):
        for i in (self.row-1, self.row, self.row+1):
            if 0 <= i < self.board.rows:
                for j in (self.col-1, self.col, self.col+1):
                    if (0 <= j < self.board.cols) and not (i==self.row and j==self.col):
                        yield self.board.board[i][j]

    def is_number(self):
        return 0 < self.value <= 8
    def is_flag(self):
        return self.flagged
    def is_empty(self):
        return self.value == 0
    def is_mine(self):
        return self.value == 9
    def show_number(self):
        self.configure(number, text=' '+str(self.value)+' ')
    def update_fg(self):
        self.configure(fg=colors[self.value])

    def reveal(self):
        if self.is_mine() or self.is_flag() or self.revealed:
            return
        self.revealed = True
        if self.is_empty():
            self.configure(empty)
            self.reveal_adjacent()
        else:
            self.show_number()
        self.board.to_reveal -= 1

    def reveal_adjacent(self):
        for adj in self.gen_adjacent():
            if not adj.revealed:
                adj.reveal()

    def add_mine(self):
        self.value = 9
        for adj in self.gen_adjacent():
            if not adj.is_mine():
                adj.value += 1
                adj.update_fg()

    def remove_mine(self):
        self.value = 0
        for adj in self.gen_adjacent():
            if adj.is_mine():
                self.value += 1
            else:
                adj.value -= 1
                adj.update_fg()
        self.update_fg()

    def on_left_click(self):
        def can_chord():
            flags = 0
            chord = True
            for adj in self.gen_adjacent():
                if adj.is_flag():
                    if not adj.is_mine():
                        chord = False
                    flags += 1
            if flags == self.value:
                if not chord:
                    self.board.lose()
                else:
                    return True
            return False

        if self.board.clicks == 0:
            if self.is_mine():
                self.board.move_mine(self)
            self.board.timer.start()
        self.board.clicks += 1
        if self.is_flag() or (self.is_empty() and self.revealed):
            return
        if self.is_number() and self.revealed and can_chord():
            self.reveal_adjacent()
        elif self.is_mine():
            self.board.lose()
        else:
            self.reveal()
        if self.board.to_reveal == 0:
            self.board.update()
            self.board.win()

    def on_right_click(self):
        if not self.revealed:
            self.configure(default if self.is_flag() else flag)
            self.flagged = not self.flagged

    def reset(self):
        self.value = 0
        self.revealed = False
        self.flagged = False
        self.configure(default)

class Board(tk.Frame):
    def __init__(self, parent, timer):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.timer = timer
        self.rows = 10
        self.cols = 10
        self.hidden_rows = 0
        self.hidden_cols = 0
        self.mines = 9
        self.clicks = 0
        self.to_reveal = (self.rows * self.cols) - self.mines
        self.board = self.init_board()
        self.rand_board()

    def init_board(self):
        return [[Space(self, i, j) for j in range(self.cols)] for i in range(self.rows)]

    def rand_board(self):
        mines = self.mines
        while mines != 0:
            row, col = randint(0, self.rows-1), randint(0, self.cols-1)
            if not self.board[row][col].is_mine():
                mines -= 1
                self.board[row][col].add_mine()
        self.apply_to_range(Space.update_fg)

    def change_size(self, new_rows, new_cols, new_mines):
        if new_cols < self.cols:
            self.shrink_cols(new_cols)
        else:
            self.expand_cols(new_cols)
        if new_rows < self.rows:
            self.shrink_rows(new_rows)
        else:
            self.expand_rows(new_rows)
        self.mines = new_mines
        self.reset()

    def apply_to_range(self, function, row_min=0, row_max=None, col_min=0, col_max=None):
        row_max = self.rows if row_max == None else row_max
        col_max = self.cols if col_max == None else col_max
        for row in self.board[row_min:row_max]:
            for space in row[col_min:col_max]:
                function(space)

    def shrink_cols(self, new_cols):
        self.hidden_cols += self.cols - new_cols
        self.apply_to_range(Space.grid_remove, col_min=new_cols)
        self.cols = new_cols

    def shrink_rows(self, new_rows):
        self.hidden_rows += self.rows - new_rows
        self.apply_to_range(Space.grid_remove, row_min=new_rows)
        self.rows = new_rows

    def expand_cols(self, new_cols):
        all_cols = self.cols + self.hidden_cols
        self.apply_to_range(Space.grid, col_max=min(new_cols, all_cols))
        for i in range(self.rows):
            self.board[i].extend([Space(self, i, j) for j in range(all_cols, new_cols)])
        self.hidden_cols = 0 if new_cols > all_cols else max(0, all_cols-new_cols)
        self.cols = new_cols

    def expand_rows(self, new_rows):
        all_rows = self.rows + self.hidden_rows
        self.apply_to_range(Space.grid, row_max=min(new_rows, all_rows))
        for i in range(all_rows, new_rows):
            self.board.append([Space(self, i, j) for j in range(self.cols)])
        self.hidden_rows = 0 if new_rows > all_rows else max(0, all_rows-new_rows)
        self.rows = new_rows

    def win(self):
        self.timer.stop()
        print("You win")

    def lose(self):
        self.timer.stop()
        print("You lose")
        self.reveal_all()

    def reveal_all(self):
        for row in self.board[:self.rows]:
            for space in row[:self.cols]:
                if space.is_mine():
                    space.configure(flag)
                elif space.is_number():
                    space.show_number()
                else:
                    space.configure(empty)
        self.parent.update()

    def move_mine(self, space):
        space.remove_mine()
        row, col = randint(0, self.rows-1), randint(0, self.cols-1)
        while (space.row == row and space.col == col) or space.is_mine():
            row, col = randint(0, self.rows-1), randint(0, self.cols-1)
        self.board[row][col].add_mine()

    def reset(self):
        self.timer.reset()
        self.apply_to_range(Space.reset)
        self.to_reveal = (self.rows * self.cols) - self.mines
        self.clicks = 0
        self.rand_board()
