import tkinter as tk
import subprocess
import os



class App:
    def __init__(self, master):
        self.master = master
        self.process = None

        self.status_label = tk.Label(master, text="Not Running", bg="red", width=50, height=5)
        self.status_label.pack()
        self.button_start = tk.Button(master, text="Start", command=self.start, width=50, height=5)
        self.button_start.pack()
        self.button_stop = tk.Button(master, text="Stop", command=self.stop, width=50, height=5)
        self.button_stop.pack()
        self.button_log = tk.Button(master, text="Show Log", command=self.update_log, width=50, height=5)
        self.button_log.pack()
        self.button_clear = tk.Button(master, text="Clear Log", command=self.clear_log, width=50, height=5)
        self.button_clear.pack()
        self.log = tk.Text(master)
        self.log.pack()

    def start(self):
        self.process = subprocess.Popen(["python", "gametracker.py"])
        self.status_label.config(text="Running", bg="green")

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.status_label.config(text="Not Running", bg="red")

    def update_log(self):
        os.startfile("spikes.txt")
        self.stop()

    def clear_log(self):
        with open("spikes.txt", "w") as f:
            f.write("")

root = tk.Tk()
app = App(root)
root.mainloop()

