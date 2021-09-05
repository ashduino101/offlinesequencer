from tkinter import *
import tkinter
import time
root = Tk()
canvas = Canvas(root, height=1080, width=1000000000)
playlineid = canvas.create_line(100, 0, 100, 1080, width ='2', fill='blue')
sequenceplaying = True
root.mainloop()
while sequenceplaying:
    canvas.move(playlineid, 100, 0)
    time.sleep(0.1)
