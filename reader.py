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
        self.name = name
        self.listbox = Listbox(self)
        self.listbox.grid(row=0, column=11, sticky="nsew")
        self.listbox.bind('<Double-1>',self.printnum)
        self.load_into_listbox()
        self.grid(row=1, column=0, sticky="nsew")
        self.create_widgets()
    
    def printnum(self,evt):
        cs = self.listbox.curselection()
        self.ch = self.listbox.get(cs)-1
       # self.canvas.delete("all")
        #self.destroy()
        #self.scrollbar.destroy()   
        #self.image_frame.destroy()
        #self.canvas.destroy()
        #self.canvas = None
        for w in self.image_frame.winfo_children():
            w.destroy()
        self.canvas.yview_moveto(0)
        #self.grid(row=1, column=0, sticky="nsew")
       # self.create_widgets()
        self.load_images()
        #print(self.listbox.get(cs))

    def load_into_listbox(self):
        mangalen = len(os.listdir(f"{self.name}"))
        print("Manga len: ",mangalen)
        for i in range(mangalen):
            self.listbox.insert(END, i+1)

    def create_widgets(self):
        # Create a canvas to hold the images
        self.canvas = tk.Canvas(self,width=800,height=700)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar   
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.image_frame, anchor="nw")
        # Load and display images
        self.load_images()

        # Bind canvas to configure scroll region
        #self.canvas.bind("<Configure>", self.on_frame_configure)

    def custom_key_for_sort(self,path):
        print(path)
        if(path[1] == "."):
            return path[0]

    def load_images(self):
        #image_paths = ["test/valami.jpg", "test/valami.jpg", "test/valami.jpg"]  # Example paths
        impath = f'{self.name}/{self.ch}'
        imfiles = os.listdir(impath)
        images = [i for i in range(len(imfiles))]
        total_height = 0
        width = 600
        self.images = []
        print("--------------------------------------")
        for i, path in enumerate(images):
            print(path)
            image = Image.open(f'{impath}/{path}.png')
            height = int(image.height * (width/image.width))
            total_height += height
            image = image.resize((width,height), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(image)
            label = tk.Label(self.image_frame, image=tk_image)
            label.image = tk_image
                # Place images in grid layout
            label.grid(row=i, column=0, sticky="nsew")
            self.images.append(tk_image)
            #label.pack(expand=True,fill=tk.BOTH)
        self.image_frame.update_idletasks()
        #self.canvas.configure(scrollregion=(0,0,width,total_height))
       # self.image_frame.configure(width=width,height=total_height)
        self.canvas.configure(scrollregion=(0,0,width,total_height))
    def on_frame_configure(self, event):
        # Update canvas scroll region when the size of the image frame changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
