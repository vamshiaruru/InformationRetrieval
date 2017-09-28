"""
Class to build Inverted Index.
"""
import shelve
from contextlib import closing
import math
import os
from datetime import datetime


class InvertedIndexBuilder(object):
    DICTIONARY = 'dictionary2.db'
    LENGTH = 'length2.db'
    file_list = list()
    CORPUS = "./static/corpus/"
    # todo strip punctuation, may be use nltk for tokenization!

    def get_files(self):
        """
        Get all .txt files from ./corpus folder
        :return: None
        """
        for fileName in os.listdir(self.CORPUS):
            if fileName.endswith(".txt"):
                self.file_list.append(os.path.join('./static/corpus/', fileName))

    def weighted_index(self):
        """
        Builds a dictionary containing words as primary keys with values being
        the posting lists. Each posting list consists of the document and the
        frequency of that word in term. We calculate term frequency of a term
        with respect to a document as 1 + log(tf) and update the dictionary.

        we need to use closing() because, to use with, a iterator needs to
        have __exit__ method defined. Closing defines it for us.

        Note that, we can't modify the contents of db in place. Hence we need
        to retrieve the posting list, modify it and then save it again.

        All that is left is to normalize the dictionary, but for that we need
        length of each document.
        :return: None
        """
        self.get_files()
        with closing(shelve.open(self.DICTIONARY)) as db:
            for file_name in self.file_list:
                with open(file_name) as f:
                    words = f.read().split()
                    for word in words:
                        word = word.lower().strip()
                        if word in db:
                            old_posting = db[word]
                            if file_name in old_posting:
                                old_posting[file_name] += 1
                            else:
                                old_posting.update({file_name: 1})
                            db[word] = old_posting
                        else:
                            db[word] = {file_name : 1}
            for word in db.iterkeys():
                for document in db[word]:
                    tf = 1 + math.log(db[word][document], 10)
                    old_posting = db[word]
                    old_posting[document] = tf
                    db[word] = old_posting

    def length_of_document(self):
        """
        finds weighted length of each document and fills it into a new shelve.
        Each document is considered
        a vector with words as dimensions and the tf associated as the value
        corresponding to that dimension.
        Therefore length of vector is square root of sum of tfs associated
        with the document.
        :return: None
        """
        with closing(shelve.open(self.DICTIONARY)) as db:
            with closing(shelve.open(self.LENGTH)) as length:
                for document in self.file_list:
                    temp_list = list()
                    for word in db.iterkeys():
                        if document in db[word]:
                            temp_list.append(db[word][document])
                    if len(temp_list):
                        vector_length = 0
                        for tf in temp_list:
                            vector_length += math.pow(tf, 2)
                        vector_length = math.pow(vector_length, 0.5)
                        length.update({document: vector_length})


if __name__ == '__main__':
    ib = InvertedIndexBuilder()
    now_time = datetime.now()
    print now_time
    ib.weighted_index()
    print datetime.now() - now_time
    now_time = datetime.now()
    print now_time
    ib.length_of_document()
    print datetime.now() - now_time
