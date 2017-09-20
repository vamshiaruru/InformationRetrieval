import requests
from bs4 import BeautifulSoup as bs
import downloader

r = requests.get("http://science.howstuffworks.com/space-channel.htm")
soup = bs(r.text)
for span in soup.findAll("span", {"class": "h3"}):
    links = span.find_all('a')
    for link in links:
        downloader.downloader(link['href'])
