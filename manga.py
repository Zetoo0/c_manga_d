import requests
import os
import sys
import time

class Manga:
    baseurl = "https://api.mangadex.dev"
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
        resp = requests.get(
            f"{Manga.baseurl}/manga",
            params={"title": title},
        )
        _id = resp.json()["data"][0]["id"]
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
