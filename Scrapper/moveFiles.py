"""
A small script to move all text files to a new folder :p
"""
import shutil
import os
from unidecode import unidecode


def remove_non_ascii(non_ascii):
    return unidecode(unicode(non_ascii, encoding="utf-8"))

source = './'
destination = './corpus'

files = os.listdir(source)

for f in files:
    if f.endswith('.txt'):
        with open(f, 'r') as fileName:
            fileData = fileName.read()
        fileData = remove_non_ascii(fileData)
        with open(f, 'w') as fileName:
            fileName.write(fileData)
        try:
            shutil.move(f, destination)
        except shutil.Error:
            pass