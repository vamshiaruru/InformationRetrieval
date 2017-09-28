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
    """
    This class defines all the search methods. It is the one that is exposed
    to Flask (for GUI).
    ;query: String, the query entered by user.
    ;query_score: a dictionary containing scores for each word query_word. The
    score is tf-idf score.
    ;stop_word : a list that contains all the query_words whose df is greater
    than 500. They are considered stop words, and are given score of zero unless
    specifically told otherwise.
    ;weighted : a boolean that checks whether the scores are calculated by the
    tf-idf scores or the scores given by the user.
    ;top_corrections : a dict containing top_corrections for all the words in
    query that have zero df.
    ;boolean_results : set of documents which satisfy boolean search model.
    """
    query = None
    query_score = dict()
    DOCUMENT_NUMBER = 690
    weighted = False
    stop_word = []
    top_corrections = dict()
    boolean_results = set()

    def __init__(self, input_query, **kwargs):
        self.query = input_query
        self.top_corrections = {}
        if kwargs.get("query_score"):
            # query_score is teh dictionary that is given by the user which
            # contains custom scores for each words. In that case we don't
            # need to calculate scores at all.
            self.query_score = kwargs.get("query_score")
            self.weighted = True
        else:
            self.query_score = {}

    def query_score_calculator(self, words):
        """
        This method updates the query_score dictionary with the score for each
        word. The score is calculated by tf-idf-cosine normalization for
        query_words. If the user supplies the scores for each words (
        determined by checking the weighted boolean), there is nothing left to do
        in this method, So we simply return. It also fills the boolean results
        set. Any document in boolean results set should be at the top of
        results list.
        1) First, term frequency of each term in the query is calculated.
        2) Df, idf are calculated with respect to the inverted index. if the
        df > 500, it is considered a stop word and added to the stop_words
        list and it's score is zero
        3) we consider each query a vector with dimensions as words and score
        corresponding to each word is used to calculate vector length
        4) score of each word is divided with this vector length to normalize
        and query_score is updated to contain updated scores.
        :param words: list of query_words
        :return:
        """
        if self.weighted:
            return
        self.query_score.update(Counter(words))
        first = True
        for key in self.query_score.iterkeys():
            with closing(shelve.open("dictionary2.db")) as db:
                if first:
                    first = False
                    post_set = set(db.get(key, {}).keys())
                    self.boolean_results = set.union(self.boolean_results,
                                                     post_set)
                else:
                    post_set = set(db.get(key, {}).keys())
                    self.boolean_results = set.intersection(self.boolean_results,
                                                            post_set)
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
        """
        Calculates cosine score for query_words. It also adds query_word to
        query_corpus. If the word was already present in the corpus,
        it increases its value by 1.
        It also populates the stop_word list of this class so as to let the
        user know what are the stop-words.
        Uses heapq.sort to get the top 20 items.
        :return: Top 20 documents with highest score
        """
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
