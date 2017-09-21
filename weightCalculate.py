import shelve
from contextlib import closing
import math


NUMBER_OF_DOCUMENTS = 694
with closing(shelve.open('dictionary.db')) as db:
    for word in db.iterkeys():
        # df = len(db[word])
        for document in db[word]:
            tf = 1 + math.log(db[word], 10)
            # idf = 1 + math.log(NUMBER_OF_DOCUMENTS/df, 10)
            db[word][document] = tf
