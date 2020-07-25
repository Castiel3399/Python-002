
#使用beautifulSoap版本解析猫眼电影

import csv
import random
import urllib

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent


class CatMovies(object):

    def __init__(self, url,header):
        self.url = url
        self.header = header

    def spiderCatMovie(self):
        resopnse=requests.get(self.url,headers=self.header)
        bs_info=bs(resopnse.text,'html.parser')
        print(bs_info)
        # for tags in bs_info.find_all('div'):
        #     print(tags)
        for tags in bs_info.find_all('div',attrs={'class':'movie-hover-info'}):
            childtag=tags.find_all('div',attrs={'class':'movie-hover-title'})
            filmName=childtag[0].find('span',attrs={'class':'name'}).text
            filmScore=childtag[0].text.strip().split('\n')[-1]
            filmType=childtag[1].text.replace('\n','').split(':')[1].strip()
            filmStar=childtag[2].text.replace('\n','').split(':')[1].strip()
            yield[
                filmName,
                filmScore,
                filmType,
                filmStar
            ]
    def exportCSV(self,catFilm):
        with open('CatFilm.csv', "a+", newline='') as file:
            csv_file = csv.writer(file)
            for row in catFilm:
                csv_file.writerow(row)






if __name__ == '__main__':
    ua=UserAgent()
    header = {'User-Agent': ua.random}
    myurl = 'https://maoyan.com/films?catId=3&showType=2'

    result=CatMovies(myurl,header)
    film=result.spiderCatMovie()
    result.exportCSV(film)
