import wx
import sys
import deserialize_from_binary as seqconvert
import ntpath
import subprocess
import pkg_resources
from tkinter import *
from tkinter import filedialog
import note_dict
import color_dict
import librosa
##########################
# Credits:
# Slach
# Murtada58
# The Python discord and StackExchange for answers to my obscure questions
# Sorry to all of you for so many questions about tkinter and weird issues, and thanks for your time
##########################

note_ids = []

def create_note(note_type, length, ntime, instrument, volume):
    note_color = (color_dict.setcolor(str(instrument)))
    notey = ((' '.join(note_dict.notedict[noteprocess] for noteprocess in str(note_type).split())).split(' '))
    note = int(notey[0])*12
    print(ntime)
    print(note)
    print(length)
    print(volume)
    note_ids.append(canvas.create_rectangle((int(ntime) * 16) + 100, note, (int(ntime)*16) + 100 + (length * 16), note + 12,
                            fill=note_color, tags=[note_color, 'note']))


# Get display resolution for canvas/window sizes
display = wx.App(False)
displaywidth, displayheight = wx.GetDisplaySize()

# install needed libraries
required = {'wxpython', 'protobuf', 'turtle', 'tk', 'playsound'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


def clearall():
    canvas.delete('note')


def loadsequence(sequenceloaddir):
    clearall()
    # Thanks to Murtada58 for this part

    class Note:
        def __init__(self, notetype, nlength, ntime, ninstrument, nvolume):
            self.class_type = "Note"
            self.note_type = notetype
            self.length = nlength
            self.time = ntime
            self.instrument = ninstrument
            self.volume = nvolume
    # Markers are NYI
    # class Markers():
    #    def __init__(self, time, setting, instrument, value, blend):
    #        self.class_type = "Markers"
    #        self.note_type = note_type
    #        self.length = length
    #        self.time = time
    #        self.instrument = instrument
    #        self.volume = volume
    # Will be added soon
    # class Settings():
    #    def __init__(self, class_type, note_type, length, time, instrument, volume):
    #        self.class_type = "Settings"
    #        self.note_type = note_type
    #        self.length = length
    #        self.time = time
    #        self.instrument = instrument
    #        self.volume = volume

    sheet = []
    note_number = -1
    note_type = 0
    length = 0
    time = 0
    instrument = 0
    volume = 0
    with open(sequenceloaddir, "r") as file:
        for line in file:
            line = line[:-1].strip().split(": ")
            if line[0] == "type":
                note_type = line[1]
            elif line[0] == "length":
                length = float(line[1])
            elif line[0] == "time":
                time = float(line[1])
            elif line[0] == "instrument":
                instrument = int(line[1])
            elif line[0] == "volume":
                volume = float(line[1])
            elif line[0] == "notes {":
                note_number += 1
                if note_number > 0:
                    # print(note_type, length, time, instrument, volume)
                    create_note(note_type, length, time, instrument, volume)
                    sheet.append(Note(note_type, length, time, instrument, volume))
                    note_type = 0
                    length = 0
                    time = 0
                    instrument = 0
                    volume = 0
    print(note_ids)


def playsequence():
    canvas.moveto(playlineid, 96, 0)
    moveline()

def moveline():
    global play
    canvas.move(playlineid, 10, 0)
    print(list(canvas.find_overlapping(*canvas.bbox(playlineid, 'note'))))
    play = root.after(100, moveline)


def savefile():
    print('nyi')

def opensequence():
    textfile = filedialog.askopenfilename(title="Open Sequence JSON File", filetypes=[('Text Sequences', '*.txt'), ('Text Sequences', '*.json')])
    loadsequence(textfile)
def importsequence():
    filetoparse = filedialog.askopenfilename(title="Open Sequence Binary File", filetypes=[('Binary Sequences', '*.sequence')])
    filetoparsename = (ntpath.basename(filetoparse)).split('.')[0]
    seqconvert.parsesequence(filetoparse)
    loadsequence('./converted/' + filetoparsename + '.sequence.txt') # yes I know this is jank

def export_mp3():
    print('nyi')

def export_wav():
    print('nyi')

def export_ogg():
    print('nyi')

def export_mid():
    print('nyi')

def stopsequence():
    print(play)
    root.after_cancel(play)
    canvas.moveto(playlineid, 96, 0)


root = Tk()

root.title('OfflineSequencer')
root.iconbitmap('./assets/icon.ico')
root.state("zoomed")

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=clearall)
filemenu.add_command(label="Open", command=opensequence)
filemenu.add_command(label="Save", command=savefile)
filemenu.add_command(label="Import", command=importsequence)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

exportmenu = Menu(menubar, tearoff=0)
exportmenu.add_command(label="Export MP3", command=export_mp3)
exportmenu.add_command(label="Export WAV", command=export_wav)
exportmenu.add_command(label="Export OGG", command=export_ogg)
exportmenu.add_command(label="Export MID", command=export_mid)
menubar.add_cascade(label="Export", menu=exportmenu)

playmenu = Menu(menubar, tearoff=0)
playmenu.add_command(label="Current Sequence...", command=playsequence)
playmenu.add_command(label="Stop", command=stopsequence)
menubar.add_cascade(label="Play", menu=playmenu)

root.config(menu=menubar)

frame = Frame(root, width=1000000000, height=displayheight)
canvas = Canvas(frame, height=displayheight, width=1000000000, scrollregion=(0, 0, 1000000, 500))
hbar = Scrollbar(frame, orient=HORIZONTAL)
hbar.pack(side=BOTTOM, fill=X)
hbar.config(command=canvas.xview)
vbar = Scrollbar(frame, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.configure(bg='#45474C')
canvas.pack(side=LEFT, expand=True, fill=BOTH)
frame.pack(side=LEFT, expand=True, fill=BOTH)
w = 100
bw = 100
h = 0
canvasobjects = []
while w < 1000000:
    canvasobjects.append(canvas.create_line(w, 0, w, displayheight, width='1', tags='grid'))
    canvasobjects.append(canvas.create_line(bw, 0, bw, displayheight, width='2', tags='grid'))
    w = w + 16
    bw = bw + 256

while h < displayheight:
    canvasobjects.append(canvas.create_line(0, h, 1000000, h, width='1', tags='grid'))
    h = h + 12
print(canvasobjects)
# 125080 and above are notes
playlineid = canvas.create_line(100, 0, 100, displayheight, width='2', fill='blue')
print(playlineid)
root.mainloop()
# canvas.move(playlineid, 100, 0)
# time.sleep(0.1)
