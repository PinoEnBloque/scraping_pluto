import requests
import csv
from entities import Movie

class PlutoTV:
    def __init__(self) -> None:
        ################## TESTING VARS ################## !!
        self.other_types = set()
        ##################################################
        self.payloads_movies = list()
        self.payloads_series = list()
        self._scraping()
        self._export()

    def _scraping(self):
        TOKEN = { 'Authorization' : 'Bearer' + requests.get(url=Utils.TOKEN['url'], params=Utils.TOKEN['params']).json()['sessionToken']}
        categories = requests.get(url=Utils.CATEGORIES['url'], params=Utils.CATEGORIES['params'], headers=TOKEN).json()
        for category in categories['categories']:
            for item in category['items']:
                if item['type'] == 'movie' : self._payload_movie(item)
                else: self.other_types.add(item['type']) # !!

        ################# TESTING PRINTS ################# !!
        if self.other_types: print('FOUND OTHER PAYLOAD TYPES : ', self.other_types)
        ##################################################

    def _payload_movie(self, rawdata):
        payload_movie = Movie(
            id       = rawdata['_id'],
            title    = rawdata['name'],
            synopsis = rawdata['summary'],
            rating   = rawdata['rating'],
            images   = [{ 'Type' : 'Banner', 'Url' : rawdata['featuredImage']['path'], 
                          'Type' : 'Cover', 'Url' : rawdata['covers'][0]['url'] }],
            genres   = [rawdata['genre']]
        ).model_dump()
        print('> INSERT MOVIE :', payload_movie['title'])
        self.payloads_movies.append(payload_movie)

    def _export(self):
        FILE_NAME = 'plutotv_scraping.csv'
        headers   = self.payloads_movies[0].keys()
        with open(FILE_NAME, 'w', newline='', encoding='UTF8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for payload in self.payloads_movies: writer.writerow(payload)
        print(f"\nEXPORTED TO '{FILE_NAME}'!")

class Utils:
    # Easily obtain Bearer token via query
    TOKEN = { 
        'url'   : 'https://boot.pluto.tv/v4/start',
        'params' : {"appName":"web","appVersion":"5.109.0-6577a51c82bdba0d9a0a2bab4950dd43d469ea83","clientID":"2b8283e5-fd59-497a-b225-86b02e133d5d","clientModelNumber":"1.0.0"}
    }
    # Categories include items with the params key "includeItems"
    CATEGORIES = {
        'url'   : 'https://service-vod.clusters.pluto.tv/v4/vod/categories',
        'params' : {"includeItems":"true","includeCategoryFields":"iconSvg","offset":"1000","page":"1","sort":"number^%^3Aasc"}
    }

if __name__ == '__main__': 
    execute = PlutoTV()
