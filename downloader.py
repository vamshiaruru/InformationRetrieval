"""
This module defines downloader helper function to scrap text from given link.
We use requests module to send requests to the server and BeautifulSoup to
parse the response.
"""
import requests
from bs4 import BeautifulSoup
# from string import printable as ascii_characters


def downloader(link):
    """
    This is a helper function to scrap date from the link.
    :param link: link to an article that is to be scrapped
    :return: None
    """
    print link
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    # printable = set(ascii_characters)
    file_name = "{}.txt".format(soup.title.string.encode('utf-8'))
    with open(file_name, 'w') as f:
        for line in soup.find_all('p')[:-10]:
            try:
                f.write(line.text.encode('utf-8'))
                f.write("\n")
            except AttributeError:
                pass
