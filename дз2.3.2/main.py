import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

client = MongoClient('mongodb+srv://useralina:123@project1.wut54bm.mongodb.net/?appName=project1')


url='https://quotes.toscrape.com/'
response=requests.get(url)
soup=BeautifulSoup(response.text,'lxml')

quotes=soup.find_all('span',class_='text')
authors=soup.find_all('small',class_='author')
tags=soup.find_all('div', class_='tags')

"""
for i in range(0, len(quotes)):
    print('\n'+quotes[i].text)
    print(f'Author: {authors[i].text}')
    if i < len(tags):
        tags_for_quote = tags[i].find_all('a', class_='tag')
        for tag in tags_for_quote:
            print(tag.text)
""" 

def write_to_file(filename, lst):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(lst, f, ensure_ascii=False, indent=4)


all_quotes=[]
for quote, author, tag_block in zip(quotes, authors, tags):
    tags_for_quote = [tag.text for tag in tag_block.find_all('a', class_='tag')]
    quote_data = {
        "tags": tags_for_quote,
        "author": author.text,
       "quote": quote.text
    }
    all_quotes.append(quote_data)

write_to_file('quotes.json', all_quotes )

db = client["hw"]
quotes_collection = db["quotes"]

with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

quotes_collection.insert_many(quotes_data)



author_links = [a['href'] for a in soup.select('.author + a')]
all_authors=[]
for link in author_links:
    author_url='https://quotes.toscrape.com'+ link
    author_response=requests.get(author_url)
    author_soup=BeautifulSoup(author_response.text,'lxml')

    fullname=author_soup.find('h3',class_='author-title')
    born_date=author_soup.find('span',class_='author-born-date')
    born_location=author_soup.find('span',class_='author-born-location')
    description=author_soup.find('div',class_='author-description')

    author_data={
        "fullname":fullname.text.strip(),
        "born_date":born_date.text.strip(),
        "born_location":born_location.text.strip(),
        "description":description.text.strip()
    }
    all_authors.append(author_data)

write_to_file('authors.json', all_authors )

authors_collection = db["authors"]

with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)

authors_collection.insert_many(authors_data)
