import reader
import tkinter as tk
import glob
import os
import manga
from dotenv import load_dotenv
import sys

def auth(username,pw,clientkey,secretkey):
    return manga.Manga.authenticate(username=username,passw=pw,client_key=clientkey,secret_key=secretkey)


load_dotenv(".env")
user_n = os.getenv("UNAME")
pw = os.getenv("PASSWORD")
[client_key,secret_key] = (os.getenv("CLIENT_KEY"),os.getenv("SECRET_KEY"))
if(client_key == "" or secret_key == "" or user_n == "" or pw == ""):
    print("There is no lenne client or secret_key or username or password")
    sys.exit(0)
else:
    acc_token,refresh_token = auth(user_n,pw,client_key,secret_key)
    print("Access token successfully arrived")
print("--------------------------------------")
#print(manga.Manga.getMangaRelationList("JoJo"))
#print(manga.Manga.rateManga("Gintama",acc_token,10))
#print(manga.Manga.getMyRatings(acc_token))
#print(manga.Manga.getReadingHistory(acc_token))
#print(manga.Manga.getLoggedUserCustomList(acc_token))
#manga.Manga.getMangaVolsAndChapters("Gintama")
print(manga.Manga.getReadingListByStatus(acc_token,"reading"))
#print(manga.Manga.addMangaToReadList("Haruka Reset",acc_token,"reading"))
"""root = tk.Tk()
root.title("Manga Reader")
root.geometry("1920x1080")
        #root.grid_rowconfigure(0, weight=1)
        #root.grid_columnconfigure(0, weight=1)
app = reader.MangaReader(name="Gintama",ch=2,master=root)
app.mainloop()
"""
#for fila in glob.glob("Gintama/1/*.png"):
 #   print(fila)
    #with open(os.path.join(os.getcwd(),fila),'r') as f:
     #   print(f)