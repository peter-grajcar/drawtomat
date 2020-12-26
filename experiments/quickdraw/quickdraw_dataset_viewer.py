#!/usr/local/bin/python3.8
import ndjson
import pprint
from tkinter import *

pp = pprint.PrettyPrinter(width=100, compact=True)
data = []
data_size = 0
words = []

with open("quickdraw-dataset/categories.txt") as f:
    for word in f.readlines():
        words.append(word[:-1])


def load_data(word):
    global data, data_size
    data = []
    try:
        with open(f"quickdraw-dataset/dataset/{word}.ndjson") as f:
            for text in f.readlines():
                json_data = ndjson.loads(text)[0]
                data.append(json_data)
                # pp.pprint(data)
    except:
        print("cannot open the file")
    data_size = len(data)


master = Tk()
master.title("Quick, Draw! Viewer")

canvas = Canvas(master, width=500, height=500)
canvas.pack()

frame = Frame(master, relief=RAISED, borderwidth=1)
frame.pack(fill="both")

index_label_text = StringVar()
index_label = Label(frame, textvariable=index_label_text)
index_label.pack(side="right")


def draw(data):
    canvas.delete("all")
    strokes = data["drawing"]
    for stroke in strokes:
        for i in range(len(stroke[0]) - 1):
            canvas.create_line(
                stroke[0][i] / 4,
                stroke[1][i] / 4,
                stroke[0][i + 1] / 4,
                stroke[1][i + 1] / 4,
            )
    canvas.create_text(10, 450, anchor="nw", text=f"word: {data['word']}")
    canvas.create_text(10, 470, anchor="nw", text=f"country: {data['countrycode']}")


data_index = 0
load_data(words[0])
if data:
    draw(data[data_index])
    index_label_text.set(f"{data_index + 1}/{data_size}")


def prev_picture(*args):
    global data_index
    if data_index > 0:
        data_index -= 1
    draw(data[data_index])
    index_label_text.set(f"{data_index + 1}/{data_size}")


def next_picture(*args):
    global data_index
    if data_index + 1 < data_size:
        data_index += 1
    draw(data[data_index])
    index_label_text.set(f"{data_index + 1}/{data_size}")


def save_picture():
    with open(f"quickdraw-dataset/saved/{word.get()}.ndjson", "a") as f:
        print(ndjson.dumps([data[data_index]]), file=f)
    print(f"Saved {word.get()}")


def change_word(*args):
    global data_index
    load_data(word.get())
    data_index = 0
    index_label_text.set(f"{data_index + 1}/{data_size}")
    draw(data[data_index])


prev_btn = Button(frame, text="Prev", command=prev_picture)
prev_btn.pack(side="left", padx=20)
save_btn = Button(frame, text="Save", command=save_picture)
save_btn.pack(side="left", padx=20)
next_btn = Button(frame, text="Next", command=next_picture)
next_btn.pack(side="left", padx=20)

word = StringVar()
word.set(words[0])
menu = OptionMenu(frame, word, *words)
menu.configure(width=20, activebackground="red")
menu.pack(side="right")
word.trace("w", change_word)

master.bind("<Left>", prev_picture)
master.bind("<Right>", next_picture)

mainloop()

