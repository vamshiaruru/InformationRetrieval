import shelve
from contextlib import closing
import math
import os


def weight(temp_list):
    squared_tf = 0
    for i in temp_list:
        squared_tf += math.pow(i, 2)
    return math.pow(squared_tf, 0.5)


def length_calculator():
    file_list = list()
    for fileName in os.listdir('./corpus/'):
        if fileName.endswith(".txt"):
            file_list.append(os.path.join('./corpus/', fileName))

    length = {}
    for document in file_list:
        temp_list = []
        with closing(shelve.open('dictionary.db')) as db:
            for word in db.keys():
                if document in db[word]:
                    temp_list.append(db[word][document])
        if len(temp_list) == 0:
            continue
        print document
        length.update({document: weight(temp_list)})
    return length
