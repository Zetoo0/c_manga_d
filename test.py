import requests
import sys
import os
import io
from PIL import Image
import climage
import time
import manga
#Now you can only download chapters for you given manga
#but later my idea that it'll list you mangas by 
#search and then you can select one of them

#print(sys.argv[1]) 
title = "SandLand"
url = "https://api.mangadex.org"

#m_anga = manga_wtf.Manga(title)
#manga_id = manga_wtf.Manga.getManga(title)["data"][0]["id"]
#print(manga_id)
#print(chapter["id"] for chapter in manga_wtf.Manga.getManga(title)["data"]) 
#mangaList = manga_wtf.Manga.testmod(["Harem"],["Action"],"en")
#for manga in mangaList["data"]:
    #xprint(f'EN:{manga["attributes"]["title"]["en"]}')#
#c#hapterList = manga_wtf.Manga.getChaptersNormallyWithPaginationUwU(manga_id)
#print(chapterList)
#print(f'len:{len(chapterList)}')
#print(chapter["id"] for chapter in chapterList)
#print(chapterList)
#print(len(chapterList))
#for chapter in chapterList["data"]:
  #  print(chapter["attributes"]["chapter"])
#print(chapterList["data"][0]["attributes"]["chapter"])

#include = ["Action"]
#exclude = ["Harem"]
#asd = manga_wtf.Manga.getMangasWithIncludedAndExcludedTags(include,exclude,"en")
#namaes = [chapter["attributes"]["title"]["en"] for chapter in asd["data"]]
while True:
  rand_manga = manga.Manga.getRandomManga()
  print(rand_manga["data"]["attributes"]["title"]["en"])
  time.sleep(0.1)