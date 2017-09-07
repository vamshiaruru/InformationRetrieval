import requests
from bs4 import BeautifulSoup
from time import sleep


def downloader(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    while soup.title.string.encode('utf-8')[:5] == "Too M":
        print "here, sleeping"
        sleep(30)
        r = requests.get(link)
        soup = BeautifulSoup(r.text)
    file_name = "file_{}.txt".format(soup.title.string.encode('utf-8')[:5])
    print file_name
    with open(file_name, 'w') as f:
        for line in soup.find_all('p'):
            if line.string:
                f.write(line.string.encode('utf-8'))
                f.write("\n")
