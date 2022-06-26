from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk


def image_open():

    file = filedialog.askopenfilename(filetypes=[("image file", "*.png *.jpg"), ("all files", "*.*")])
    if file:
        if file.endswith(".png") or file.endswith(".jpg"):
            img = Image.open(file)
            return img
        else:
            messagebox.showinfo("בחירת תמונה", "קובץ לא נתמך")
    else:
        return


def board_open():

    file = filedialog.askopenfilename(filetypes=[("board file", "*.csv")])

    return file


def image_save():
    file = filedialog.asksaveasfilename(filetypes=(("png files", "*.png"), ("all files", "*.*")))
    if file.endswith(".png"):
        pass
    else:
        file = file + ".png"
    return file


def dir_ch():
    dir_t = filedialog.askdirectory()
    print(dir_t)
    return dir_t


def board_save():
    file = filedialog.asksaveasfilename(filetypes=[("board file", "*.csv"), ("all files", "*.*")])
    if file:
        if file.endswith(".csv"):
            pass
        else:
            file = file + ".csv"
        return file
    else:
        return


def load_image(file_name):

    img = Image.open(file_name)

    return img
