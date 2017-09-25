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
from EditDistace import EditDistance


class Searcher(object):
    query = None
    query_score = dict()
    DOCUMENT_NUMBER = 690
    weighted = False
    stop_word = []
    top_corrections = dict()

    def __init__(self, input_query, **kwargs):
        self.query = input_query
        self.top_corrections = {}
        if kwargs.get("query_score"):
            self.query_score = kwargs.get("query_score")
            self.weighted = True
        else:
            self.query_score = {}

    def query_score_calculator(self, words):
        if self.weighted:
            return
        self.query_score.update(Counter(words))
        for key in self.query_score.iterkeys():
            with closing(shelve.open("dictionary2.db")) as db:
                self.query_score[key] = 1 + math.log(self.query_score[key], 10)
                df = len(db.get(key, {}))
                if df == 0:
                    idf = 0
                elif df > 500:
                    idf = 0
                    self.stop_word.append(key)
                else:
                    idf = math.log(self.DOCUMENT_NUMBER/df)
                self.query_score[key] *= idf
        vector_length = 0
        for key in self.query_score.iterkeys():
            vector_length += math.pow(self.query_score[key], 2)
        vector_length = math.pow(vector_length, 0.5)
        if vector_length == 0:
            return
        for key in self.query_score.iterkeys():
            self.query_score[key] /= vector_length

    def cosine_score(self):
        query_words = [word.lower().strip() for word in self.query.split()]
        self.query_score_calculator(query_words)
        db = shelve.open("dictionary2.db")
        length = shelve.open("length2.db")
        qc = shelve.open("query_corpus.db")
        for word in query_words:
            if self.query_score[word]:
                if word in qc:
                    prev = qc[word]
                    qc[word] = prev + 1
                else:
                    qc[word] = 1
            elif not self.query_score[word] and word not in self.stop_word:
                self.top_corrections[word] = EditDistance().top_corrections(word)
        scores = {}
        for query_term in self.query_score.iterkeys():
            posting_list = db.get(query_term, {})
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
        db.close()
        length.close()
        qc.close()
        return sorted_scores[0:20]

if __name__ == "__main__":
    query = "elon musk"
    query_score = {"elon": 0.15, "musk": 0.25}
    search = Searcher(query, query_score=query_score)
    print search.cosine_score()
    print search.query_score
