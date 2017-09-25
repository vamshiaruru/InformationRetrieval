import os
from unidecode import unidecode
import re


def remove_non_ascii(non_ascii):
    return unidecode(unicode(non_ascii, encoding="utf-8"))

source = './'

files = os.listdir(source)

for fileName in files:
    with open('./'+fileName) as f:
        name = remove_non_ascii(f.name)
        os.rename(f.name, name)
        if " | HowStuffWorks" in f.name:
            new_name = re.sub(' /| HowStuffWorks', "", name)
            os.rename(name, new_name)
