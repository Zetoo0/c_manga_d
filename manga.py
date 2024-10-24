import requests
import os
import sys
import time
import tkinter as tk
from PIL import ImageTk,Image
import concurrent.futures
#import pytesseract

class ChapterOrder:
    def __init__(self,chapter):
        self.chapter = chapter

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
        print("Kapott title: " + title)
        resp = requests.get(f'{Manga.baseurl}/manga',params={"title" : title.lower(),"offset" : 0})
        print("Manga Id: ",resp.json()["data"][0])    
        return resp.json()["data"][0]["id"]


    @staticmethod
    def getChapters(id,currOfs):
        """
        Get the chapters with offset 20
        """
        #languages = ["en"]
       # order = ChapterOrder("asc")
        print(f"offset:{currOfs}")
        #manga = Manga.getManga(title)
        chaptersResp = requests.get(
            f'{Manga.baseurl}/manga/{id}/feed',
            params={"translatedLanguage[]": "en","order[chapter]":"asc","limit":20,"offset":currOfs},
       )    
        print(chaptersResp.json())   
        return chaptersResp.json()
    

    def getLatestChapter(id):
        """
        Get the latest chapter
        """
        #manga = Manga.getManga(title)
        chaptersResp = requests.get(
            f'{Manga.baseurl}/manga/{id}/feed',
            params={"translatedLanguage[]": "en","order[chapter]":"desc","limit":1},
       )    
        print(chaptersResp.json())   
        return chaptersResp.json()

    @staticmethod
    def downloadLatestChapter(title):
        _id = Manga.getMangaId(title)
        print("id: ",_id)
        chapter = Manga.getLatestChapter(_id)
        chapterlen = len(os.listdir(title))
        os.makedirs(f"{title}/{chapterlen}",exist_ok=True)
                #print(chapters[i]["id"])
        print("-----------------------------")
        print(chapter['data'][0]['id'])
        resp = requests.get(f"{Manga.baseurl}/at-home/server/{chapter['data'][0]['id']}")
        host = resp.json()["baseUrl"]
        hash = resp.json()["chapter"]["hash"]
        dat_saver = resp.json()["chapter"]["data"]
        print(hash)
            # print(dat_saver)
        pagei = 0
        for page in dat_saver:
            print("for real")
            img = requests.get(f"{host}/data/{hash}/{page}")
                #  img_pil = Image.open(io.BytesIO(img.content))
            ch_path = f"{title}/{chapterlen}/{pagei}.png"
                #    img_pil.save(ch_path)
            with open(ch_path, mode="wb") as f:
                print("Irni kellene a képet????")
                f.write(img.content)
                pagei+=1        

    @staticmethod
    def startDownloadAndSaveAllChapter(title):
        _id = Manga.getMangaId(title)
        chapters = Manga.getChaptersNormallyWithPaginationUwU(_id)
        print("----------------------------------")
        ch_len = len(chapters)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for ii,downloaded in enumerate(chapters):
                futures.append(executor.submit(Manga.downloadChapter,title,downloaded,ii))
            for future in concurrent.futures.as_completed(futures):
                future.result()

    @staticmethod
    def downloadChapter(title,downloaded,ii):
        for chapter in downloaded:
                print("For?,")
                os.makedirs(f"{title}/{ii}",exist_ok=True)
                #print(chapters[i]["id"])
                resp = requests.get(f"{Manga.baseurl}/at-home/server/{chapter['id']}")
                host = resp.json()["baseUrl"]
                hash = resp.json()["chapter"]["hash"]
                dat_saver = resp.json()["chapter"]["data"]
                print(hash)
            # print(dat_saver)
                pagei = 0
                for page in dat_saver:
                    print("for real")
                    img = requests.get(f"{host}/data/{hash}/{page}")
                #  img_pil = Image.open(io.BytesIO(img.content))
                    ch_path = f"{title}/{ii}/{pagei}.png"
                #    img_pil.save(ch_path)
                    with open(ch_path, mode="wb") as f:
                        print("Irni kellene a képet????")
                        f.write(img.content)
                    pagei+=1
                ii+=1

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
        publication demographics: shounen, seinen, shoujo, josei
        manga status: completed, ongoing, cancelled, hiatus
        """
        #TODO
        #resp = requests.get(f'{Manga.baseurl}/manga'"""params={'status' : status, 'publicationDemographic' : publicationDemographic}""")
        #return resp.json()
    
    @staticmethod
    def getChaptersNormallyWithPaginationUwU(id)->list:
        offset = 0
        pageList = []
        pagedCh = Manga.getChapters(id,offset)
       # print(pagedCh)
       # print(pagedCh)
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
        print(username,passw)
        credentials = {"grant_type" : "password","username" : username,"password" : passw,"client_id" : client_key,"client_secret" : secret_key}
        resp = requests.post(Manga.authurh,data=credentials).json()
        print(resp)
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
    def rateManga(manga,token,rate):
        """
        Rate manga from 1-10
        """
        id = Manga.getMangaId(manga)
        resp = requests.post(f'{Manga.baseurl}/rating/{id}',headers={'Authorization' : f'Bearer {token}'},json={"rating" : rate})
        return resp
    
    @staticmethod
    def getMyRatings(token):
        resp = requests.get(f'{Manga.baseurl}/rating',headers={"Authorization" : f'Bearer {token}'})
        return resp

    @staticmethod
    def deleteRating(manga,token):
        id = Manga.getMangaId(manga)
        resp = requests.delete(f'{Manga.baseurl}/rating/{id}',headers={'Authorization' : f'Bearer {token}'})

    @staticmethod
    def getReadingList(token):
        resp = requests.get(f'{Manga.baseurl}/list',headers={"Authorization" : f'Bearer {token}'})
        print(resp)

    @staticmethod
    def getMangaReadingStatus(token,manga):
        id = Manga.getMangaId(manga)
        resp = requests.get(f'{Manga.baseurl}/manga/{id}/status',headers={"Authorization" : f'Bearer {token}'})
        return resp['data']

    @staticmethod
    def getMangaVolsAndChapters(manga):
        id = Manga.getMangaId(manga)
        resp = requests.get(f'{Manga.baseurl}/manga/{id}/aggregate')
        print(resp)

    @staticmethod
    def getMangaRelationList(manga):
        id = Manga.getMangaId(manga)
        resp = requests.get(f'{Manga.baseurl}/manga/{id}/relation')

    @staticmethod
    def getReadingHistory(token):
        resp = requests.get(f'{Manga.baseurl}/user/history', headers={"Authorization" : f'Bearer {token}'})
       ##print(resp.json()[])
        return resp.json()

    @staticmethod
    def getUserDetails(token):
        resp = requests.get(f'{Manga.baseurl}/user/me',headers={"Authorization" : f'Bearer {token}'})
        return resp

    @staticmethod
    def createCustomList(token,listName,visibility):
        options = {"name" : listName,"visibility" : visibility}
        resp = requests.post(f'{Manga.baseurl}/list',headers={"Authorization" : f'Bearer {token}'},json=options)
        print(f'{listName} created')
        return resp.json()["data"]["id"]#Maybe I could save into a json file? TODO
    
    @staticmethod
    def getLoggedUserCustomList(token):
        resp = requests.get(f'{Manga.baseurl}/user/list',headers={"Authorization" : f'Bearer {token}'})
        return resp
    @staticmethod
    def addMangaToCustomList(token,list_id,mangaAdd):
        mangaAdd = Manga.getMangaId(mangaAdd)
        resp = requests.post(f'{Manga.baseurl}/list/{list_id}',headers = {"Authorization" : f'Bearer {token}'})
        version = resp.json()["data"]["attributes"]["version"]
        r_put = requests.put(f'{Manga.baseurl}/list/{list_id}',headers={"Authorization" : f'Bearer {token}'},json={"manga":mangaAdd,"version" : version})
        print(r_put)
    @staticmethod
    def removeMangaFromCustomList(token,list_id,mangaRemove):
        mangaRemove = Manga.getMangaId(mangaRemove)
        resp = requests.post(f'{Manga.baseurl}/list/{list_id}',headers = {"Authorization" : f'Bearer {token}'})
        version = resp.json()["data"]["attributes"]["version"]
        r_put = requests.put(f'{Manga.baseurl}/list/{list_id}',headers={"Authorization" : f'Bearer {token}'},json={"manga" : mangaRemove, "version":version})


    @staticmethod
    def getReadingListByStatus(token,status):
        resp = requests.get(f'{Manga.baseurl}/manga/status',headers={"Authorization" : f'Bearer {token}'},json={"status":status})
        print(resp)#TODO
    
    @staticmethod
    def getMangaBayesianRating(manga):
        _id = Manga.getMangaId(manga)
        resp = requests.get(f'{Manga.baseurl}/statistics/manga', json={"manga" : _id})
        return  resp.json()["statistics"][_id]["rating"]["bayesian"]
    
