#!/usr/bin/env pipenv-shebang
# -*- coding: utf-8 -*-
import moviepy.editor as MpEditor
import wand.image as WndImage
import PIL.Image as PILImage
import wand as wnd
# import io
import io
import numpy as np
import time
import argparse
# import tkFileDialog
from tkinter import filedialog
from tkinter import *
from moviepy.editor import *
from PIL import ImageDraw
from random import choice
import os
# from Tkinter import *

class VideoProcess():

    def __init__(self):
        self.Clip = None
        # self.clipPath = None

    def make_dummy(self):
        blob = io.BytesIO()
        width = self.Clip.w
        height = self.Clip.h
        image = PILImage.new("RGB", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((10,10,300,300), fill="red", outline="red")
        del draw
        image.save(blob, format='JPEG')
        return image

    def rescaler(self, img):
        blob = io.BytesIO()
        with WndImage.Image(blob=img) as img:
            img.format = 'jpeg'
            size = img.size
            coefBounds = range(self.lowerBound, self.upperBound)
            coef_x = choice(coefBounds)
            coef_y = choice(coefBounds)
            if choice((0, 1)) == 0:
                ch = ('div', 'mul')
                x_size = size[0]//coef_x
                y_size = size[1]//coef_y
            else:
                ch = ('mul', 'div')
                x_size = size[0]//coef_x
                y_size = size[1]//coef_y
            img.liquid_rescale(x_size, y_size)
            img.sample(size[0], size[1])
            print(size[0], size[1])
            img_bin = img.make_blob('jpeg')
            blob = io.BytesIO(img_bin)
            # blob = io.BytesIO(b'{}'.format(img_bin))
        return blob


    def image_adaptor(self, imarray):
        # magick_home=os.getcwd() + os.sep + 
        # magick_home = "C:\Program Files\ImageMagick-7.0.9-Q16"
        # os.environ["PATH"] += os.pathsep + magick_home + os.sep
        # os.environ["MAGICK_HOME"] = magick_home
        # os.environ["MAGICK_CODER_MODULE_PATH"] = magick_home + os.sep + "modules" + os.sep + "coders"
        print(os.environ["MAGICK_CODER_MODULE_PATH"])
        blob = io.BytesIO()
        inpImage = PILImage.fromarray(imarray, 'RGB')
        inpImage.save(blob, format='JPEG')
        blob2 = self.rescaler(blob.getvalue())
        blob2.seek(0)
        img = PILImage.open(blob2)
        imarray = np.fromstring(img.tobytes(), dtype=np.uint8)
        try:
            imarray = imarray.reshape((img.size[1], img.size[0], 3))
        except ValueError as err:
            print(str(err))
            img = self.make_dummy()
            imarray = np.fromstring(img.tobytes(), dtype=np.uint8)
            imarray = imarray.reshape((img.size[1], img.size[0], 3))
            # print(imarray)
            # imarray = 0
        return imarray


    def main(self):
        write_data = time.strftime("%I%M%S")
        self.Clip = MpEditor.VideoFileClip(self.clipPath)
        breakpoint
        self.Clip = self.Clip.fl_image(self.image_adaptor)
        out_string = str(self.clipPath).rsplit(".")[0] + "__CAS-{}".format(write_data) + ".mp4"
        print(out_string)
        self.Clip.write_videofile(out_string, codec='libx264', audio_codec='aac')



class GUI(VideoProcess):
    """make the GUI version of this command that is run if no options are
    provided on the command line"""
    def __init__(self):
        self.lowerBound = None
        self.lowerBound = None
        VideoProcess.__init__(self)
        self.main_window()

    def Entry1_Callback(self, event):
        self.insert_bound1.selection_range(0, END)

    def Entry2_Callback(self, event):
        self.insert_bound2.selection_range(0, END)



    def button_go_callback(self):
        try:
            self.lowerBound = int(min(self.insert_bound1.get(), self.insert_bound2.get()))
            self.upperBound = int(max(self.insert_bound1.get(), self.insert_bound2.get()))
        except ValueError:
            print('Non integer range input, use default 4 and 5')
            self.insert_bound1.delete(0, 'end')
            self.insert_bound1.insert(END, '4')
            self.insert_bound2.delete(0, 'end')
            self.insert_bound2.insert(END, '5')
            self.lowerBound = int(min(self.insert_bound1.get(), self.insert_bound2.get()))
            self.upperBound = int(max(self.insert_bound1.get(), self.insert_bound2.get()))
        self.clipPath = self.entry.get()
        self.main()


    def button_browse_callback(self):
        """ What to do when the Browse button is pressed """
        filename = filedialog.askopenfilename()
        self.entry.delete(0, END)
        self.entry.insert(0, filename)

    def main_window(self):
        root = Tk()
        frame = Frame(root)
        frame.pack()
        statusText = StringVar(root)
        statusText.set("Working")

        label = Label(root, text="Video file: ")
        label.pack()
        self.insert_bound1 = Entry(root, width=10)
        self.insert_bound2 = Entry(root, width=10)
        self.insert_bound1.insert(END, 'lower bound')
        self.insert_bound2.insert(END, 'higher bound')
        self.insert_bound1.bind("<FocusIn>", self.Entry1_Callback)
        self.insert_bound2.bind("<FocusIn>", self.Entry2_Callback)
        self.entry = Entry(root, width=50)
        self.entry.pack()
        separator = Frame(root, height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

        button_go = Button(root,
                        text="Go",
                        command=self.button_go_callback)
        button_browse = Button(root,
                            text="Browse",
                            command=self.button_browse_callback)
        button_exit = Button(root,
                            text="Exit",
                            command=sys.exit)
        self.insert_bound1.pack()
        self.insert_bound2.pack()
        button_go.pack()
        button_browse.pack()
        button_exit.pack()

        separator = Frame(root, height=2, bd=1, relief=SUNKEN)
        separator.pack(fill=X, padx=5, pady=5)

        self.message = Label(root, textvariable=statusText)
        self.message.pack()
        mainloop()

if __name__ == "__main__":
    RescalerInstance = GUI()