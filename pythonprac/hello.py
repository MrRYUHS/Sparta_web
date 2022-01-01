import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#old_content > table > tbody > tr')

for tr in trs:
    a_tag = tr.select_one('td.title > div > a')
    a_tag1 = tr.select_one('td.point')
    a_tag2 = tr.select_one('td:nth-child(1) > img')

    if a_tag2 is not None:
        rank = a_tag2['alt']
        title = a_tag.text
        star = a_tag1.text
        doc = {
            'rank':rank,
            'title':title,
            'star':star
        }
        db.movies.insert_one(doc)