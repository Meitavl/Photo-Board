
# ------------------------------------------
# App for making board for speech terapy
#
# email: meitav.livne@gmail.com
# ------------------------------------------

from tkinter import *
from tkinter import colorchooser, simpledialog, messagebox
from PIL import ImageGrab, Image
import File_selector
import photo_set
import os
import csv
import math

import button_image

image_album = []
edit = 0
fr_th = 0
slc = None
copy = 0
loc = 0
def_frame = 0


def resize_image(img_num):

    # Resize image size according to user definition
    width = simpledialog.askinteger("Width", "Insert width in cm:")
    height = simpledialog.askinteger("Height", "Insert height in cm:")
    if width is not None and height is not None:
        if width > 0 and height > 0:
            image_album[img_num].photo_resize(math.floor(width / 0.0264583333), math.floor(height / 0.0264583333))
        elif width is not None and height is not None:
            messagebox.showinfo("Info", "You must insert new dimensions")
        else:
            messagebox.showinfo("Info", """
    No change was made
    Dimension must be bigger then 0
            """)
    else:
        messagebox.showinfo("Info", "You must insert new dimensions")
    show_label()


def add_image():
    global slc, copy, loc

    # Adding image to board , limited to 6 images
    slc, copy, loc = None, 0, 0
    if len(image_album) < 6:
        try:
            image = File_selector.image_open()
            if image:
                image_set = photo_set.PhotoSet(image, len(image_album))
                image_album.append(image_set)
            else:
                messagebox.showinfo("Info", "Image not selected")
        except AttributeError:
            print(' ')
    else:
        messagebox.showinfo("Adding Image", "Limited to 6 image")

    show_label()


def rotate_image(img_num):

    # Rotate image according to user definition
    angle = simpledialog.askinteger("Rotate", "Insert angle to rotate:")
    if angle:
        image_album[img_num].photo_rotate(angle)
    else:
        messagebox.showinfo("Info", "No change was made")

    show_label()


def replace(img_num):

    # Replacing an existing image with a new image
    image = File_selector.image_open()
    if image:
        image_set = photo_set.PhotoSet(image, img_num)
        image_album[img_num] = image_set
    else:
        messagebox.showinfo("Info", "No change was made")

    show_label()


def remove(img_num):
    global slc, copy, loc

    slc, copy, loc = None, 0, 0
    # Removing an existing image from the board
    image_album.pop(img_num)
    for i in range(img_num, len(image_album)):
        image_album[i].num = i

    show_label()


def forget():

    # Clean GUI from the old widgets
    for label in root.winfo_children():
        label.destroy()


def color():

    # Choosing color using colors window
    my_color = colorchooser.askcolor()[1]
    color_bg = my_color

    return color_bg


def bd(img_num):

    # Frame border thickness changes according to the user definition
    bd_frame = simpledialog.askinteger("Frame thickness", "Insert frame thickness")
    if bd_frame:
        if bd_frame > 0:
            image_album[img_num].bd = bd_frame
            image_album[img_num].img_frame_size()
        else:
            messagebox.showinfo("Info", """
No change
Thickness need to be bigger then 0
        """)
    else:
        messagebox.showinfo("info", "No change")

    show_label()


def bg(img_num):

    # Frame background color changes according to the user definition
    bg_frame = color()
    if bg_frame:
        image_album[img_num].bg = bg_frame
    else:
        messagebox.showinfo("Info", "No color selected")

    show_label()


def cpy_app():

    # Copy frame format between existing images
    global slc, copy, loc

    show_label()
    copy = 1
    loc = 0


def loc_img():

    # Replacing between images on the board
    global slc, loc, copy

    show_label()
    loc = 1
    copy = 0


def frame_edit(img_num):

    # Frame editing GUI
    global fr_th
    fr_th = Toplevel()
    fr_th.geometry('+1300+50')
    fr_th.overrideredirect(True)
    edit.destroy()

    fr_th.wm_attributes('-transparentcolor', 'white')

    frame_frame = Frame(fr_th, bd=0, bg='white')
    frame_frame.grid(row=0, column=0)
    bd_button = Button(frame_frame, borderwidth=0, bg='white', image=thick_button_img, command=lambda: bd(img_num))
    bd_button.grid(row=0, column=0)
    bg_button = Button(frame_frame, borderwidth=0, bg='white', image=color_button_img, command=lambda: bg(img_num))
    bg_button.grid(row=1, column=0)

    fr_th.mainloop()


def edit_image(img_num):

    # Edit image GUI
    global edit

    edit = Toplevel()
    # edit.title('Edit')
    edit.geometry('+1300+50')
    edit.overrideredirect(True)
    edit.wm_attributes('-transparentcolor', 'white')

    edit_frame = Frame(edit, bd=0, bg="white")
    edit_frame.grid(row=0, column=0)

    button_rot_image = Button(edit_frame, borderwidth=0, bg="white", image=rotate_button_img, command=lambda: rotate_image(img_num))
    button_rot_image.grid(row=0, column=0)

    button_res_image = Button(edit_frame, borderwidth=0, bg="white", image=resize_button_img, command=lambda: resize_image(img_num))
    button_res_image.grid(row=1, column=0)

    button_rep = Button(edit_frame, borderwidth=0, bg="white", image=replace_loc_button_img, command=lambda: replace(img_num))
    button_rep.grid(row=2, column=0)

    button_remove = Button(edit_frame, borderwidth=0, bg="white", image=remove_button_img, command=lambda: remove(img_num))
    button_remove.grid(row=3, column=0)

    button_frame_edit = Button(edit_frame, borderwidth=0, bg="white", image=frame_edit_button_img, command=lambda: frame_edit(img_num))
    button_frame_edit.grid(row=4, column=0)

    button_ext_edit = Button(edit_frame, borderwidth=0, bg="white", image=close_button_img, command=edit.destroy)
    button_ext_edit.grid(row=5, column=0)

    edit.mainloop()


def edit_image_event(event):

    # Getting location by right mouse click
    try:
        edit.destroy()
    except AttributeError:
        print('')
    widget = event.widget
    info = widget.grid_info()
    row = info['row']
    column = info['column']
    img_num = img_num_loc(row, column)

    if img_num is not None:
        edit_image(img_num)


def select_image(event):

    # Getting location by left mouse click
    global slc, copy, loc, image_album

    if str(type(event.widget)) == "<class 'tkinter.Label'>" and (copy == 1 or loc == 1):
        widget = event.widget
        info = widget.grid_info()
        row = info['row']
        column = info['column']
        img_num = img_num_loc(row, column)
        if copy == 1:
            image_album[img_num].image_att_copy(image_album[slc])
            image_album[img_num].img_frame_size()
        else:
            image_album[slc].num = img_num
            image_album[img_num].num = slc
            image_album = sorted(image_album, key=lambda x: x.num)
        slc = None
        copy = 0
        loc = 0

        show_label()

    elif str(type(event.widget)) == "<class 'tkinter.Label'>":
        widget = event.widget
        info = widget.grid_info()
        row = info['row']
        column = info['column']
        img_num = img_num_loc(row, column)
        image_bg = image_album[img_num].bg
        image_album[img_num].bg = "red"
        slc = img_num

        show_label()
        image_album[img_num].bg = image_bg


def img_num_loc(row, column):

    # Translate image location to image number
    for item in range(len(image_album)):
        if image_album[item].row == row and image_album[item].column == column:
            return item


def save_board_img():

    # Save board image for printing
    global def_frame

    result = File_selector.image_save()

    if result:
        root.update()
        x = 55 + def_frame.winfo_rootx()
        y = def_frame.winfo_rooty()
        x1 = x + def_frame.winfo_width() * 1.25
        y1 = y + def_frame.winfo_height() * 1.25
        try:
            ImageGrab.grab().crop((x, y, x1, y1)).save(result, quality=100)
            os.startfile(result, "print")
        except ValueError:
            messagebox.showinfo('info', 'Image not saved')




def save_board():

    # Save board for future working
    file = File_selector.board_save()

    if file:
        file = file[:-4] + "/"

        os.makedirs(file, exist_ok=True)

        # Writing to csv

        f = open(file + "board.csv", "w", newline="")

        writer = csv.writer(f)

        # Saving images

        for num in range(len(image_album)):
            image_album[num].real_img.save(file + str(image_album[num].num) + ".png", quality=100)
            tup = (image_album[num].num, image_album[num].bd,
                   image_album[num].angle, image_album[num].bg, image_album[num].size)
            writer.writerow(tup)

        f.close()
    else:
        pass


def load_board():

    # Load older board for working
    global image_album

    file = File_selector.board_open()

    if file:
        image_album = []
        file_tmp = file

        file = open(file, "r")

        count = 0

        reader = csv.reader(file)
        file_tmp = file_tmp[:-9]

        for row in reader:
            if count < 6:
                count = count + 1
                num = ""
                image = File_selector.load_image(file_tmp + row[0] + ".png")
                number = []
                for n in row[4][:]:
                    if n.isdigit():
                        num = num + n
                    elif num != "":
                        number.append(int(num))
                        num = ""
                    else:
                        print("")
                image_set = photo_set.PhotoSet(image, int(row[0]))
                image_album.append(image_set)
                image_album[int(row[0])].num, image_album[int(row[0])].bd, image_album[int(row[0])].bg =\
                    int(row[0]), int(row[1]), row[3]
                image_album[int(row[0])].photo_resize(number[0], number[1])
                image_album[int(row[0])].photo_rotate(int(row[2]))
            else:
                pass

        file.close()
    else:
        pass
    show_label()


def show_label():

    # Show images on GUI
    global def_frame

    forget()

    button_frame = Frame(root, bd=0, bg="#3486eb")
    button_frame.grid(column=0, row=0, rowspan=5)
    button_add_image = Button(button_frame, borderwidth=0, bg='#3486eb', border=0, image=add_button_img, command=add_image)
    button_add_image.grid(column=0, row=0, pady=10)
    exit_button = Button(button_frame, borderwidth=0, bg='#3486eb', image=exit_button_img, command=root.destroy)
    exit_button.grid(column=0, row=5, pady=10)
    load_button = Button(button_frame, borderwidth=0, bg='#3486eb', image=load_board_button_img, command=load_board)
    load_button.grid(column=0, row=1, pady=10)

    if len(image_album):
        def_frame = Frame(root, bd=0, bg="#3486eb")
        def_frame.grid(column=1, row=0, padx=20, pady=10, columnspan=len(image_album), rowspan=2)
        save_button = Button(button_frame, bd=0, bg="#3486eb", image=save_image_button_img, command=save_board_img)
        save_button.grid(column=0, row=2, pady=10)
        save_board_button = Button(button_frame, bd=0, bg="#3486eb", image=save_board_button_img, command=save_board)
        save_board_button.grid(column=0, row=3, pady=10)

    if 3 <= len(image_album):
        def_frame.grid_configure(columnspan=3)

    if slc is not None:
        size_pxl_to_cm = tuple([math.ceil(x) for x in [x * 0.0264583333 for x in image_album[slc].size]])
        s_text_size = "Image size: " + str(size_pxl_to_cm)
        s_text_bd = "Frame thickness: " + str(image_album[slc].bd)
        status = Label(root, bg="#3486eb", text=s_text_size + " " + s_text_bd, anchor=SW)
        status.grid(column=1, row=4, columnspan=3, sticky=E + W)


    if slc is not None and len(image_album) > 1:
        copy_button = Button(root, borderwidth=0, bg="#3486eb", image=copy_ap_button_img, command=cpy_app)
        copy_button.grid(column=1, row=3)
        loc_button = Button(root, borderwidth=0, bg="#3486eb", image=cha_loc_button_img, command=loc_img)
        loc_button.grid(column=2, row=3)

    try:
        edit.destroy()
    except AttributeError:
        print('')

    for num in range(len(image_album)):
        # save photo grid place
        if num < 3:
            image_album[num].img_grid(0, num)
        elif 3 <= num < 6:
            image_album[num].img_grid(2, num - 3)
        else:
            messagebox.showinfo("Info", "Limited to 6 Images")

        if num < 6:
            # Frame for image
            frame = Frame(def_frame, bd=0, height=image_album[num].frame_size[1], bg=image_album[num].bg)
            frame.grid(column=image_album[num].column, row=image_album[num].row, pady=10, padx=20)

            # showing image on screen
            image_label = Label(frame, borderwidth=0, image=image_album[num].photo)
            image_label.grid(column=image_album[num].column, row=image_album[num].row,
                             pady=image_album[num].bd, padx=image_album[num].bd)

            root.update()


root = Tk()
root.attributes('-fullscreen', True)
root.title('Photo Board')
root.option_add("*font", "lucida 16 bold italic")
root.config(bg='#3486eb')
# root.wm_attributes('-transparentcolor', 'white')
# root.overrideredirect(True)

add_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\add.png')
exit_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\exit.png')
load_board_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\load_board.png')
save_board_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\save_board.png')
save_image_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\save_image.png')
copy_ap_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\copy_appearance.png')
cha_loc_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\change_loc.png')
rotate_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\rotate.png')
resize_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\resize.png')
close_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\close.png')
remove_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\remove.png')
replace_loc_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\replace.png')
frame_edit_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\frame_edit.png')
thick_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\thickness.png')
color_button_img = PhotoImage(file=r'C:\Users\Meitav\Documents\GitHub\Photo-Project\color.png')


show_label()

root.bind("<Button-3>", edit_image_event)
root.bind("<Button-1>", select_image)

root.mainloop()
