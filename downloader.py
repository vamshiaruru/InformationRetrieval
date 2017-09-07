import requests
from bs4 import BeautifulSoup


def downloader(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    file_name = "file_{}.txt".format(soup.title.string[:5])
    with open(file_name, 'w') as f:
        for line in soup.find_all('p'):
            if line.string:
                f.write(line.string.encode('utf-8'))
