"""
This module calculates the tf-idf score for document. We follow lnc for this,
that means idf is not done. So we'll just calculate tf and divide the resulting
vector by length
"""

import shelve
from contextlib import closing
import math
from lengthCalculator import length_calculator
from datetime import datetime


NUMBER_OF_DOCUMENTS = 694
startTime = datetime.now()

with closing(shelve.open('dictionary.db')) as db:
    for word in db.iterkeys():
        for document in db[word]:
            tf = 1 + math.log(db[word][document], 10)
            old_dict = db[word]
            old_dict[document] = tf
            db[word] = old_dict

length = length_calculator()

with closing(shelve.open('dictionary.db')) as db:
    for word in db.iterkeys():
        for document in db[word]:
            old_dict = db[word]
            old_dict[document] = old_dict[document]/length[document]
            db[word] = old_dict

print datetime.now() - startTime