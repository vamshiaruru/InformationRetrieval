"""
This generates A dictionary with each key being a unique word present in a
pool of documents and the corresponding value being the posting list of the key.

We use 'shelve' for persistent storage. Performing operations on large
dictionary stored in-memory (RAM) is a bad idea. Shelve stores python objects
in disk.
"""
import os
import shelve
from contextlib import closing


DATABASE_NAME = 'dictionary.db'
file_list = list()
for fileName in os.listdir('./'):
    # os.listdir('directory') lists all the files in 'directory'. './' means
    # current directory.
    if fileName.endswith(".txt"):
        file_list.append(os.path.join('./', fileName))

with closing(shelve.open(DATABASE_NAME)) as dictionary:
    # we need to use closing() because shelve.open() doesn't define an
    # __exit__ method without with "with" can't be used. closing() defines
    # that method for us
    for fileName in file_list:
        with open(fileName) as f:
            words = set(f.read().split())
            # apply any new tokenization logic here
            for word in words:
                word = word.lower().strip()
                if word in dictionary:
                    # Shelve['key'] contents, if the value is a iterable
                    # python object can't be changed directly. Hence we
                    # retrieve it, mutate it and then give it back instead.
                    new_set = dictionary[word]
                    new_set.add(fileName)
                    dictionary[word] = new_set
                else:
                    # create a new set if the word is not present. We are
                    # using sets because 'and', 'or' , 'in' etc are O(1) in sets.
                    dictionary[word] = {fileName}

