import time
import tkinter as tk

class Timer(tk.Label):
    def __init__(self, parent):
        self.parent = parent
        self.label = tk.Label.__init__(self, parent, font=("Arial", 12))
        self.start_time = None
        self.after_id = None

    def start(self):
        self.start_time = time.time()
        self.update_time()

    def stop(self):
        self.start_time = None
        if self.after_id != None:
            self.after_cancel(self.after_id)

    def reset(self):
        self.secs = 0
        self.stop()

    def update_time(self):
        cur_time = time.time()
        elapsed_secs = int(cur_time - self.start_time)
        self.configure(text=str(elapsed_secs))
        self.after_id = self.after(100, self.update_time)
