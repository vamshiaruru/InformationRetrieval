import os
import shelve
from contextlib import closing


file_list = list()
for fileName in os.listdir('./'):
    if fileName.endswith(".txt"):
        file_list.append(os.path.join('./', fileName))

with closing(shelve.open('dictionary.db')) as dictionary:
    for fileName in file_list:
        with open(fileName) as f:
            words = set(f.read().split())
            for word in words:
                word = word.lower().strip()
                if word in dictionary:
                    new_set = dictionary[word]
                    new_set.add(fileName)
                    dictionary[word] = new_set
                else:
                    dictionary[word] = {fileName}

