import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MangaReader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        # Create a canvas to hold the images
        self.canvas = tk.Canvas(self,width=1280,height=720)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Add a scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((800, 300), window=self.image_frame, anchor="center")

        # Load and display images
        self.load_images()

        # Bind canvas to configure scroll region
        self.image_frame.bind("<Configure>", self.on_frame_configure)

    def load_images(self):
        image_paths = ["test/valami.jpg", "test/valami.jpg", "test/valami.jpg"]  # Example paths

        self.images = []
        for i, path in enumerate(image_paths):
            image = Image.open(path)
            tk_image = ImageTk.PhotoImage(image)
            label = tk.Label(self.image_frame, image=tk_image)
            label.image = tk_image
            # Place images in grid layout
            label.grid(row=i, column=0, sticky="nsew")

    def on_frame_configure(self, event):
        # Update canvas scroll region when the size of the image frame changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
