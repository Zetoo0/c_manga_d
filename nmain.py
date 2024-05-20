#main for project
import manga
import argparse
import os,sys,reader
import tkinter as tk
from dotenv import load_dotenv
from PIL import Image

class MangaCLI(argparse.Action):
    def __call__(self,parser,namespace,values,option_str=None):
        print(option_str)
        if(option_str == '-rm' or option_str == '--randommanga'):
            self.getRandomManga()
        elif(option_str == '-r' or option_str == '--read'):
            namae = " ".join([val for val in values])
            self.read(namae)
        elif(option_str == '-m' or option_str == '--manga'):
            self.mangatest()
        elif(option_str == '-dw' or option_str == '--download'):
            namae = " ".join([val for val in values])
            self.downloadAllChapter(namae)
        elif(option_str == '-upd' or option_str == '--updatemanga'):
            print("update???")
            namae = " ".join([val for val in values])
            self.downloadNewestChapter(namae)
        elif(option_str == '-addtolist'):
            namae = " ".join([val for val in values])
            self.addToList(namae)
        elif(option_str == '-addtocustom'):
            namae = " ".join([val for val in values])
            self.addToCustomList(namae)
        
        setattr(namespace,self.dest,values)

    def read(arg,datas):
        print("Opening manga: ",datas[0])
        root = tk.Tk()
        root.title("Manga Reader")
        root.geometry("1920x1080")
        app = reader.MangaReader(name=datas[0],master=root)#test maybe not good xd
        app.mainloop()

    def rateManga(arg,name):
        print("Rate manga: ")
        rate = input()
        manga.Manga.rateManga(manga=name,rate=rate,token=acc_token)

    def followManga(arg,name):
        manga.Manga.followManga(name,acc_token)
    def mangatest(arg,nam):
        print(nam)
      

    def addToList(arg,name):
        print("press (r) for readlist\n(p) for plan to read\n(o) for on hold\n(d) for dropped\n(r) for re-read\n(c) for completed")
        inputka = input()
        manga.Manga.addMangaToReadList(name,acc_token,statuses[inputka])

    def addToCustomList(arg,name):
        print("Custom list name:")
        inputk = input()
        manga.Manga.addMangaToCustomList(acc_token,inputk,name)

    def downloadAllChapter(arg,name):
        #print(name)
        print(f"Download {name} manga...")
        manga.Manga.startDownloadAndSaveAllChapter(name)

    def downloadNewestChapter(arg,name):
        print(f'Update {name} manga...')
        manga.Manga.downloadLatestChapter(name)

    def getRandomManga(arg):
        print(manga.Manga.getRandomManga()["data"]["attributes"]["title"]["en"])

    def readListByStatus(arg):
        pass

def auth(username,pw,clientkey,secretkey):
    return manga.Manga.authenticate(username=username,passw=pw,client_key=clientkey,secret_key=secretkey)

statuses = {'c':'completed', 'p' : 'plan_to_read', 'o' : 'on_hold', 'd' : 'dropped', 'r' : 're_reading'}
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
parser.add_argument('-dw','--download',action=MangaCLI,nargs='+')
parser.add_argument('-upd','--updatemanga',action=MangaCLI,nargs='+')
parser.add_argument('-rate','--ratemanga',action=MangaCLI,nargs='+')
parser.add_argument('-addtolist','--attest',action=MangaCLI,nargs='+')
parser.add_argument('-addtocustom','--aztest',action=MangaCLI,nargs='+')



args = parser.parse_args()