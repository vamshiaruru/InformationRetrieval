"""
This module defines downloader helper function to scrap text from given link.

We use requests module to send requests to the server and BeautifulSoup to
parse the response.
"""
import requests
import requests.exceptions as network_exception
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
    if r.status_code == FORBIDDEN_STATUS:
        # r.status_code is 403 means the website has forbidden us from scraping.
        print "forbidden from scrapping."
        return
    soup = BeautifulSoup(r.text)
    count = 0
    try:
        while r.status_code == TOO_MANY_REQUESTS:
            # In this case, just sleep for sometime and send a request again.
            if count == MAX_TRIES:
                raise network_exception
            count += 1
            print "here, sleeping"
            sleep(30)
            r = requests.get(link)
            soup = BeautifulSoup(r.text)
    except network_exception:
        # Timeout, SSL error, Proxy Error, invalid link and so on.
        print network_exception
        return

    file_name = "file_{}.txt".format(soup.title.string.encode('utf-8')[:5])
    # come-up with a better file_name by all means and change this comment when
    # done. DO NOT CHANGE THE FILE EXTENSION.
    with open(file_name, 'w') as f:
        for line in soup.find_all('p'):
            # we are finding all 'p' tags because information is usually
            # present inside paragraph tags. DON"T SCRAP THE BODY.
            if line.string:
                f.write(line.string.encode('utf-8'))
                f.write("\n")
