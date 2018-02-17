# -*- coding: utf-8 -*-
# /venv/Scripts/Python.exe
import moviepy.editor as MpEditor
import wand as wnd
import wand.image as WndImage
import StringIO
import PIL.Image as PILImage
import io
from random import choice
import numpy as np
import time
from moviepy.editor import *
import argparse
import tkFileDialog
from Tkinter import *

countFrom = 0
write_data = time.strftime("%I%M%S")

def gui():
    """make the GUI version of this command that is run if no options are
    provided on the command line"""

    def button_go_callback():

        input_file = entry.get()
        main(input_file)


    def button_browse_callback():
        """ What to do when the Browse button is pressed """
        filename = tkFileDialog.askopenfilename()
        entry.delete(0, END)
        entry.insert(0, filename)

    root = Tk()
    frame = Frame(root)
    frame.pack()

    statusText = StringVar(root)
    statusText.set("Working")

    label = Label(root, text="Video file: ")
    label.pack()
    entry = Entry(root, width=50)
    entry.pack()
    separator = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

    button_go = Button(root,
                       text="Go",
                       command=button_go_callback)
    button_browse = Button(root,
                           text="Browse",
                           command=button_browse_callback)
    button_exit = Button(root,
                         text="Exit",
                         command=sys.exit)
    button_go.pack()
    button_browse.pack()
    button_exit.pack()

    separator = Frame(root, height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

    message = Label(root, textvariable=statusText)
    message.pack()


    def inc_label(label):      
      def count():
        global countFrom
        countFrom += 1
        label.config(text=str(countFrom))
        label.after(1000, count)
      count()
 
    inc_label(message)
    mainloop()

def wand_opener(img):
    blob = io.BytesIO()
    with WndImage.Image(blob=img) as img:
        img.format = 'jpeg'
        print('width =', img.width)
        print('height =', img.height) 
        size = img.size
        coef_x = choice((2,3,4,5))
        coef_y = choice((2,3,4,5))
        if choice((0, 1)) == 0:
           ch = ('div', 'mul')
           x_size = size[0]//coef_x
           y_size = size[1]//coef_x
        else:
            ch = ('mul', 'div')
            x_size = size[0]//coef_x
            y_size = size[1]//coef_x
        img.liquid_rescale(x_size, y_size)
        img.sample(size[0], size[1])
        print(size[0], size[1])
        img_bin = img.make_blob('jpeg')
        blob = io.BytesIO(b'{}'.format(img_bin))
    return blob


def show_me_type(imarray):
    blob = io.BytesIO()
    inpImage = PILImage.fromarray(imarray, 'RGB')
    print(inpImage.size)
    inpImage.save(blob, format='JPEG')
    print(blob)
    blob2 = wand_opener(blob.getvalue())
    blob2.seek(0)
    img = PILImage.open(blob2)
    imarray = np.fromstring(img.tobytes(), dtype=np.uint8)
    print(imarray)
    imarray = imarray.reshape((img.size[1], img.size[0], 3))
    return imarray


def main(videoClip):
    x = MpEditor.VideoFileClip(videoClip)
    # x = x.subclip(0.05, x.duration)
    x = x.fl_image(show_me_type)
    x = x.resize( (1920, 1080) )
    out_string = str(videoClip).rsplit(".")[0] + "__time-{}".format(write_data) + ".mp4"
    print(out_string)
    x.write_videofile(out_string,  fps=60)

if __name__ == "__main__":
    gui()