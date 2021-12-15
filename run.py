import tkinter as tk
from timer import Timer
from board import Board
from new import Restart, Custom

window = tk.Tk()
top_frm = tk.Frame(window, width=20)
board_frm = tk.Frame(window, width=20)

timer = Timer(top_frm)
board = Board(board_frm, timer)
small = Custom(top_frm, board, "S", 10, 10, 10)
med = Custom(top_frm, board, "M", 15, 15, 40)
large = Custom(top_frm, board, "L", 16, 30, 100)
restart = Restart(top_frm, board)

top_frm.rowconfigure(0, weight=1)
top_frm.columnconfigure(3, weight=2)
top_frm.columnconfigure(4, weight=2)

small.grid(row=0, column=0)
med.grid(row=0, column=1)
large.grid(row=0, column=2)
restart.grid(row=0, column=3)
timer.grid(row=0, column=4)

top_frm.pack(fill="both")
board_frm.pack(side=tk.BOTTOM)

def quit():
    timer.stop()
    window.destroy()

window.protocol('WM_DELETE_WINDOW', quit)
window.mainloop()
