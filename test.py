import reader
import tkinter as tk
import glob
import os

root = tk.Tk()
root.title("Manga Reader")
root.geometry("1920x1080")
        #root.grid_rowconfigure(0, weight=1)
        #root.grid_columnconfigure(0, weight=1)
app = reader.MangaReader(name="Gintama",ch=2,master=root)
app.mainloop()

#for fila in glob.glob("Gintama/1/*.png"):
 #   print(fila)
    #with open(os.path.join(os.getcwd(),fila),'r') as f:
     #   print(f)