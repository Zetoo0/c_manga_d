import tkinter as tk
from tkinter import ImageTk,Image
class ReaderApplication:
    def __init__(self,manga,master):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Manga Reader")
        self.manga = manga
        self.master = master