#main for project
import manga
import argparse
import os,sys,reader
import tkinter as tk
from dotenv import load_dotenv
from PIL import Image

class MangaCLI(argparse.Action):
    def __call__(self,parser,namespace,values,option_str=None):
        #print(f'Value:{values} - Option: {option_str}')
        if(option_str == '-rm' or option_str == '--randommanga'):
            self.getRandomManga()
        elif(option_str == '-r' or option_str == '--read'):
            #print("Micsipicsi")
            self.read(values)
        elif(option_str == '-m' or option_str == '--manga'):
            self.mangatest()
            #print("vasút")
            #self.read()
        elif(option_str == '-dw' or option_str == '--download'):
            self.downloadAllChapter(values)
        
        
        setattr(namespace,self.dest,values)

    def read(arg):
        print("????")
        root = tk.Tk()
        root.title("Manga Reader")
        root.geometry("1920x1080")
        #root.grid_rowconfigure(0, weight=1)
        #root.grid_columnconfigure(0, weight=1)

        app = reader.MangaReader(master=root)
        app.mainloop()

    def addToFixedList(arg):
        pass

    def mangatest(arg,nam):
        print(nam)
    def addToCustomList(arg):
        pass

    def downloadAllChapter(arg,name):
        print(f"Download {name} manga...")
        manga.Manga.startDownloadAndSaveAllChapter(name)

    def getRandomManga(arg):
        print(manga.Manga.getRandomManga()["data"]["attributes"]["title"]["en"])

    def readListByStatus(arg):
        pass

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
#print(acc_token,refresh_token)
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--manga',action=MangaCLI)
parser.add_argument('-r', '--read',action=MangaCLI)
parser.add_argument('-rm', '--randommanga',action=MangaCLI,help="Get Random Manga",nargs=0)
parser.add_argument('-dw','--download',action=MangaCLI)

args = parser.parse_args()

#print(args)



