import requests
import os
import sys
import time
import tkinter as tk
from PIL import ImageTk,Image

class Manga:
    baseurl = "https://api.mangadex.org"
    authurh = "https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token"
    title : str
    
    def __init__(self,title):
        self.title = title
    
    @staticmethod
    def getManga(title):
        resp = requests.get(
            f"{Manga.baseurl}/manga",
            params={"title": title,"offset": 0},
        )
        return resp.json()
    
    @staticmethod
    def getMangaId(title):
        resp = requests.get(f'{Manga.baseurl}/manga',params={"title" : title,"offset" : 0})
        return resp.json()["data"][0]["id"]

    @staticmethod
    def getChapters(id,currOfs):
        """
        Get the chapters with offset 20
        """
        languages = ["en"]
        #manga = Manga.getManga(title)
        chaptersResp = requests.get(
            f'{Manga.baseurl}/manga/{id}/feed',
            params={"translatedLanguage[]": "en","limit":20,"offset":currOfs},
       )    
        #print(chaptersResp.json())   
        return chaptersResp.json()

    @staticmethod
    def startDownloadAndSaveAllChapter(title):
        #resp = requests.get(
         #   f"{Manga.baseurl}/manga",
          #  params={"title": title},
        #)"""
        _id = Manga.getMangaId(title)
        chapters = Manga.getChaptersNormallyWithPaginationUwU(_id)
        ch_len = len(chapters)

        for i in range(ch_len):
            os.makedirs(f"{title}/{i}",exist_ok=True)
            #print(chapters[i]["id"])
            resp = requests.get(f"{Manga.baseurl}/at-home/server/{chapters[i]['id']}")
            host = resp.json()["baseUrl"]
            hash = resp.json()["chapter"]["hash"]
            dat_saver = resp.json()["chapter"]["data"]
            print(hash)
        # print(dat_saver)
            for page in dat_saver:
                img = requests.get(f"{host}/data/{hash}/{page}")
            #  img_pil = Image.open(io.BytesIO(img.content))
                ch_path = f"{title}/{i}/{page}"
            #    img_pil.save(ch_path)
                with open(ch_path, mode="wb") as f:
                    f.write(img.content)        

    @staticmethod
    def getMangasWithIncludedAndExcludedTags(includeT,excludeT,lang):
        """
        Get mangas with included and excluded tags and with languages
        """
        tags = requests.get(f'{Manga.baseurl}/manga/tag').json()
        included_ids = [tag["id"] for tag in tags["data"] if tag["attributes"]["name"]["en"] in includeT]
        excluded_ids = [tag["id"] for tag in tags["data"] if tag["attributes"]["name"]["en"] in excludeT]

        filter = {
            'includedTags[]' : included_ids, 
            'excludedTags[]' : excluded_ids,
        }

        resp = requests.get(f'{Manga.baseurl}/manga', params=filter)
        return resp.json()
    
    
    @staticmethod
    def getMangasWithStatusAndPublicationDemographic(status, publicationDemographic):
        """
        Get the mangas with status and publication demographic
        publication demographics are: shounen, seinen, shoujo, josei
        manga statuses are: completed, ongoing, cancelled, hiatus
        """
        #TODO
        #resp = requests.get(f'{Manga.baseurl}/manga'"""params={'status' : status, 'publicationDemographic' : publicationDemographic}""")
        #return resp.json()
    
    @staticmethod
    def getChaptersNormallyWithPaginationUwU(id)->list:
        offset = 0
        pageList = []
        pagedCh = Manga.getChapters(id,offset)
        while len(pagedCh['data']) > 0:
            print(pagedCh["data"])
            pageList.append(pagedCh['data'])
            offset += 20
            pagedCh = Manga.getChapters(id,offset)
            time.sleep(0.1)
        #print(chaptersResp.json())   
        return pageList
    
    @staticmethod
    def getRandomManga():
        manga = requests.get(f'{Manga.baseurl}/manga/random').json()
        return manga

    @staticmethod
    def authenticate(client_key,secret_key,username,passw):
        credentials = {"grant_type" : "password","username" : username,"password" : passw,"client_id" : client_key,"client_secret" : secret_key}
        resp = requests.post(Manga.authurh,data=credentials).json()
        return (resp["access_token"],resp["refresh_token"])
    
    @staticmethod
    def addMangaToReadList(manga,token,status):
        id = Manga.getMangaId(manga)
        print(id)
        resp = requests.post(f'{Manga.baseurl}/manga/{id}/status',headers={"Authorization" : f'Bearer {token}'},json = {"status" : status})
        print(f'Response: {resp.json()["result"]}')
        print(f'Successfully added manga to reading list: {manga} - {status}')

    @staticmethod
    def followManga(manga,token):
        id = Manga.getMangaId(manga)
        resp = requests.post(f'{Manga.baseurl}/manga/{id}/follow',headers={"Authorization" : f'Bearer {token}'})

    @staticmethod
    def createCustomList(token,listName,visibility):
        options = {"name" : listName,"visibility" : visibility}
        resp = requests.post(f'{Manga.baseurl}/list',headers={"Authorization" : f'Bearer {token}'},json=options)
        print(f'{listName} created')
        return resp.json()["data"]["id"]#Maybe I could save into a json file? TODO
    
    @staticmethod
    def addMangaToCustomList(token,list_id,mangaAdd):
        mangaAdd = Manga.getMangaId(mangaAdd)
        resp = requests.post(f'{Manga.baseurl}/list/{list_id}',headers = {"Authorization" : f'Bearer {token}'})
        version = resp.json()["data"]["attributes"]["version"]

        r_put = requests.put(f'{Manga.baseurl}/list/{list_id}',headers={"Authorization" : f'Bearer {token}'},json={"manga":mangaAdd,"version" : version})

    @staticmethod
    def removeMangaFromCustomList(token,list_id,mangaRemove):
        mangaRemove = Manga.getMangaId(mangaRemove)
        resp = requests.post(f'{Manga.baseurl}/list/{list_id}',headers = {"Authorization" : f'Bearer {token}'})
        version = resp.json()["data"]["attributes"]["version"]
        r_put = requests.put(f'{Manga.baseurl}/list/{list_id}',headers={"Authorization" : f'Bearer {token}'},json={"manga" : mangaRemove, "version":version})


    @staticmethod
    def getReadingListByStatus(token,status):
        resp = requests.get(f'{Manga.baseurl}/status',headers={"Authorization" : f'Bearer {token}'},json={"status":status})
        print(resp)


#very big TODO make a manga reader with tkinter(?) or with c++/rust and with a command it's open it after that you can read the manga or its open the whole manga library of the user and the user can pick one and read
