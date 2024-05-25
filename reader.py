import tkinter as tk
import os
from tkinter import *
import glob
from PIL import Image, ImageTk


class MangaReader(tk.Frame):
    def __init__(self, master=None,name="",ch=1):
        super().__init__(master)
        self.master = master
        self.ch = ch-1
        self.page = 0
        self.name = name
        self.loaded_pages = []
        self.listbox = Listbox(self)
        self.listbox.grid(row=0, column=11, sticky="nsew")
        self.listbox.bind('<Double-1>',self.change_chapter)
        self.load_into_listbox()
        self.grid(row=1, column=0, sticky="nsew")
        self.create_widgets()

    def change_chapter(self,evt):
        cs = self.listbox.curselection()
        self.clear_widgets(cs)
        print(f'After cleared image array: {self.loaded_pages}')
        self.load_images()
        print(f'After loaded image array: {self.loaded_pages}')
        self.goto_page()

    def next_page(self):
        self.page += 1
        self.goto_page()

    def prev_page(self):
        self.page -= 1
        self.goto_page()

    def goto_page(self):
        tk_image = ImageTk.PhotoImage(self.loaded_pages[self.page])
        self.page_label.configure(image=tk_image)
        self.page_label.image = tk_image
        self.image_frame.configure(width=tk_image.width(),height=tk_image.height())
        self.canvas.yview_moveto(0)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def clear_widgets(self,cs):
        self.ch = self.listbox.get(cs)-1
        self.loaded_pages = []
        self.page = 0



    def load_into_listbox(self):
        mangalen = len(os.listdir(f"{self.name}"))
        print("Manga len: ",mangalen)
        for i in range(mangalen):
            self.listbox.insert(END, i+1)

    def create_widgets(self):
        # Create a canvas to hold the images
        self.canvas = tk.Canvas(self,width=1280,height=720)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar   
        self.scrollbar = tk.Scrollbar(self, orient="vertical",command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((200,0), window=self.image_frame, anchor="nw")
        # Load and display images
        self.load_images()
        tk_image = ImageTk.PhotoImage(self.loaded_pages[self.page])
        self.page_label = tk.Label(self.image_frame,image=tk_image)
        self.page_label.image = tk_image
        self.page_label.grid(row=0, column=0, sticky="nsew")

        self.next_btn = tk.Button(self,text="Next",command=self.next_page)
        self.next_btn.grid(row=1, column=11, sticky="nsew")
        self.prev_btn = tk.Button(self,text="Prev",command=self.prev_page)
        self.prev_btn.grid(row=2, column=11, sticky="nsew")

        ## Bind canvas to configure scroll region
        self.canvas.bind("<Configure>", self.on_frame_configure)

    def custom_key_for_sort(self,path):
        print(path)
        if(path[1] == "."):
            return path[0]

    def load_images(self):
        impath = f'{self.name}/{self.ch}'
        imfiles = os.listdir(impath)
        images = [i for i in range(len(imfiles))]
        width = 1024
        print("--------------------------------------")
        for i, path in enumerate(images):
            print(path)
            image = Image.open(f'{impath}/{path}.png')
            height = int(image.height * (width/image.width))
            image = image.resize((width,height), Image.LANCZOS)
            self.loaded_pages.append(image)
            self.image_frame.configure(width=width,height=height)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        # Update canvas scroll region when the size of the image frame changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
