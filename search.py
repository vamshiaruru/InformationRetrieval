"""
This is the script that is exposed to the GUI/user. It calls the ranking
script, takes the query and searches for it.
"""
import shelve
from contextlib import closing


if __name__ == "__main__":
    query = raw_input("Enter the query: ")
    result_documents = {}
    # using sets because convenient for set intersection
    query_words = [word.lower().strip() for word in query.split()]
    with closing(shelve.open("dictionary.db")) as dictionary:
        query_posting_list = [dictionary.get(query_word, {}) for
                              query_word in query_words]
        myDict = query_posting_list[0]
        for key, value in sorted(myDict.iteritems(), key=lambda (k, v): (v, k)):
            print "%s: %s" % (key, value)
        # result_documents = set.intersection(*query_posting_list)

    # add ranker logic i.e calculate scores based of TF,IDF or Cosine.
    # print result_documents
