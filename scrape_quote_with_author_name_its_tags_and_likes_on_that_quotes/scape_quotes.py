import requests
from bs4 import BeautifulSoup
import csv
from pandas import read_csv

URL = 'https://www.goodreads.com/quotes/?page='
n_pages = int(input("Enter no. of pages you want to scrape :"))

QUOTES = []
for i in range(n_pages):
    print('Onto Scraping Page No.', i+1)
    new_url = URL + str(i+1)
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)

    quote = soup.findAll("div", attrs={"class" : "quote"})
    print(len(quote))

    for i in range(len(quote)):
        ith_quote = quote[i]
        #print(ith_quote)

        quote_text = ith_quote.find("div", attrs={ "class" : "quoteText" })
        text = quote_text.text.split("\n")[1].strip()
        author = quote_text.span.text.strip()
        print(text)
        print(author)

        div_tags = ith_quote.find("div", attrs={ "class" : "greyText smallText left" })
        if div_tags == None:
            tags = []
        else:
            anchor_tags = div_tags.findAll('a')
            tags = [a.text for a in anchor_tags] 
        print(tags)

        anchor_likes = ith_quote.find("a", attrs={ "class" : "smallText" })
        likes = int(anchor_likes.text.replace(' likes', ''))
        print(likes)

        QUOTES.append({'author':author, 'quote':text, 'tags': tags, 'likes': likes})

with open('quotes.csv', 'w',newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['quote', 'author', 'tags', 'likes'])
    writer.writeheader()
    for q in QUOTES:
        writer.writerow(q)

df = read_csv('quotes.csv')
df.head()

