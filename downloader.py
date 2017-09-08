"""
This module defines downloader helper function to scrap text from given link.

We use requests module to send requests to the server and BeautifulSoup to
parse the response.
"""
import requests
import requests.exceptions as network_exception
from bs4 import BeautifulSoup
from time import sleep


def downloader(link):
    """
    This is a helper function to scrap date from the link. This link is
    obtained by scrapping reddit.
    :param link: link to an article that is to be scrapped
    :return: None
    """
    print link
    r = requests.get(link)
    if r.status_code == 403:
        # r.status_code is 403 means the website has forbidden us from scraping.
        print "forbidden from scrapping."
        return
    soup = BeautifulSoup(r.text)

    try:
        while r.status_code == 429:
            # This while loop is used because of Reddit's policy to not let
            # multiple requests in a quick session. The status code is 429 then.
            # In this case, just sleep for sometime and send a request again.
            print "here, sleeping"
            sleep(30)
            r = requests.get(link)
            soup = BeautifulSoup(r.text)
    except network_exception:
        # in case an error occurred while scrapping, instead of terminating the
        # entire script, just don't scrap the link. These errors include
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
