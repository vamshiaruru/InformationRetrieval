import os
from unidecode import unidecode
import re


def remove_non_ascii(non_ascii):
    return unidecode(unicode(non_ascii, encoding="utf-8"))

source = '../corpus'

files = os.listdir(source)

for fileName in files:
    with open("../corpus"+fileName) as f:
        os.rename(f.name, remove_non_ascii(f.name))
        if " | HowStuffWorks" in f.name:
            new_name = re.sub(' HowStuffWorks', "", f.name)
            os.rename(f.)