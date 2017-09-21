import requests
from bs4 import BeautifulSoup as bs
import downloader

# for i in range(1, 18):
#     link = "http://science.howstuffworks.com/space-channel.htm?page={}"\
#            .format(i)
#     r = requests.get(link)
#     soup = bs(r.text)
#     for span in soup.findAll("span", {"class": "h3"}):
#         links = span.find_all('a')
#         for link in links:
#             downloader.downloader(link['href'])

for i in range(1, 25):
    address = "https://www.livescience.com/space/{}?type=article".format(i)
    print address
    r = requests.get(address)
    soup = bs(r.text)
    for element in soup.find_all("li", {"class": "search-item line pure-g"}):
        link = element.find('a')
        downloader.downloader("https://www.livescience.com"+link['href'])
