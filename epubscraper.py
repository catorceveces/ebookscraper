from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
import tweepy

consumer_key = 'XXX'
consumer_secret = 'XXX'
access_token = 'XXX'
access_token_secret = 'XXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# web to read

on_shelves = 'https://epublibre.org/catalogo/index/0/nuevo/novedades/sin/todos'

uClient = uReq(on_shelves)
website = soup(uClient.read(), 'html.parser')
uClient.close()

# find all the books on the website

new_books = website.findAll('div', class_='span2 pad_t_20 ali_centro txt_blanco')

# create a temporary database to storage these books

minidb = 'minidb.csv'
f = open(minidb, 'w', encoding='utf-8')

# iterate over the books on the web and add them to the database

for book in new_books:
    author = book.h2.text
    title = book.h1.text
    link = book.a.get('href')

    new_entry = str(author).replace(',', '') + ',' + str(title).replace(',', '') + ',' + str(link) + '\n'

    f.write(new_entry)

f.close()

# check if the book in the temporary database is alredy exist on the permanent database
# if exists, no action; if it not, publish as tweet and adding to the permanent database

with open('minidb.csv', 'r', encoding='utf-8') as check:
    data1 = csv.reader(check)
    for element in data1:
        with open('bookdb.csv', 'r', encoding='utf-8') as control:
            data2 = csv.reader(control)
            if element not in data2:
                api.update_status(status = 'Se publicó ' + element[1] + ' de ' + element[0] + ' en EpubLibre. Entrá acá para verlo: ' + element[2] + '#epub #ebook #freebook #kindle')
                with open('bookdb.csv', 'a', newline='', encoding='utf-8') as adding:
                    writer = csv.writer(adding)
                    writer.writerow(element)
