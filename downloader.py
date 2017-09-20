"""
This module defines downloader helper function to scrap text from given link.

We use requests module to send requests to the server and BeautifulSoup to
parse the response.
"""
import requests
import requests.exceptions as network_exception
import bs4
from bs4 import BeautifulSoup
from time import sleep

TOO_MANY_REQUESTS = 429
# when we send too many requests in a very short time reddit terminates the
# request by sending this status code
FORBIDDEN_STATUS = 403
# some websites prevent scrapping by sending a forbidden status of 403
MAX_TRIES = 3
# max number of times to try to scrap from a link


def downloader(link):
    """
    This is a helper function to scrap date from the link. This link is
    obtained by scrapping reddit.
    :param link: link to an article that is to be scrapped
    :return: None
    """
    print link
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    file_name = "{}.txt".format(soup.title.string.encode('utf-8'))
    # come-up with a better file_name by all means and change this comment when
    # done. DO NOT CHANGE THE FILE EXTENSION.
    with open(file_name, 'w') as f:
        for line in soup.find_all('p'):
            text = []
            for x in line:
                if isinstance(x, bs4.element.NavigableString):
                    print x
                    text.append(x.strip().encode("utf-8"))
            # we are finding all 'p' tags because information is usually
            # present inside paragraph tags. DON"T SCRAP THE BODY.
            if line.string:
                f.write(" ".join(text))
                f.write("\n")

downloader("http://science.howstuffworks.com/space/aliens-ufos/fermi-paradox-where-heck-are-all-aliens.htm")