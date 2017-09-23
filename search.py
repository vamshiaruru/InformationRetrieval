"""
This is the script that is exposed to the GUI/user. It calls the ranking
script, takes the query and searches for it.
"""
from __future__ import division
import shelve
from contextlib import closing
import math
from collections import Counter
import heapq
import operator


class Searcher(object):
    query = None
    query_score = dict()
    DOCUMENT_NUMBER = 693

    def __init__(self, input_query):
        self.query = input_query

    def query_score_calculator(self, words):
        self.query_score.update(Counter(words))
        for key in self.query_score.iterkeys():
            with closing(shelve.open("dictionary.db")) as db:
                self.query_score[key] = 1 + math.log(self.query_score[key], 10)
                df = len(db.get(key, {}))
                if df == 0 or df > 500:
                    idf = 0
                else:
                    idf = math.log(self.DOCUMENT_NUMBER/df)
                print key, idf
                self.query_score[key] *= idf
        print self.query_score
        vector_length = 0
        for key in self.query_score.iterkeys():
            vector_length += math.pow(self.query_score[key], 2)
        vector_length = math.pow(vector_length, 0.5)
        print vector_length
        if vector_length == 0:
            return
        for key in self.query_score.iterkeys():
            self.query_score[key] /= vector_length
        print self.query_score

    def cosine_score(self):
        query_words = [word.lower().strip() for word in self.query.split()]
        self.query_score_calculator(query_words)
        db = shelve.open("dictionary.db")
        length = shelve.open("length.db")
        qc = shelve.open("query_corpus.db")
        for word in query_words:
            if word in qc:
                prev = qc[word]
                qc[word] = prev + 1
            else:
                qc[word] = 1
        scores = {}
        for query_term in self.query_score.iterkeys():
            posting_list = db.get(query_term, {})
            print query_term, self.query_score[query_term]
            for file_name in posting_list.iterkeys():
                document_score = scores.get(file_name, 0)
                document_score += self.query_score[query_term] *\
                                  posting_list[file_name]
                scores[file_name] = document_score
        for document in scores:
            scores[document] /= length[document]

        # todo implement this with heap
        scores = scores.items()
        sorted_scores = heapq.nlargest(20, scores, key=operator.itemgetter(1))
        for i in sorted_scores[0:20]:
            print i[0], i[1]

if __name__ == "__main__":
    query = raw_input("Enter the query: ")
    search = Searcher(query)
    search.cosine_score()
