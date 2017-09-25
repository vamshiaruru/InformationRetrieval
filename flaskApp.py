from search import Searcher
from flask import Flask, render_template, request
import unicodedata
app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/displayResults", methods=['POST'])
def search():
    query = request.form.get('searchBar')
    query = unicodedata.normalize('NFKD', query).encode('ascii', 'ignore')
    searcher = Searcher(query)
    results = searcher.cosine_score()
    scores = searcher.query_score
    zero_scores = searcher.top_corrections
    return render_template("displayResults.html", input_query=query,
                           results=results, scores=scores,
                           zero_scores=zero_scores)


@app.route("/displayWeightedResults", methods=['POST'])
def weighted_search():
    weights = {}
    query = request.form.get("query")
    for key in request.form:
        if key == "query":
            query = request.form[key]
            query = unicodedata.normalize('NFKD', query).encode('ascii',
                                                                'ignore')

        else:
            weights[key] = request.form[key]
            weights[key] = unicodedata.normalize('NFKD', weights[key]).encode(
                                                            'ascii', 'ignore')
            weights[key] = float(weights[key])/100

    searcher = Searcher(query, query_score=weights)
    results = searcher.cosine_score()
    scores = searcher.query_score
    zero_scores = searcher.top_corrections
    return render_template("displayResults.html", input_query=query,
                           results=results, scores=scores,
                           zero_scores=zero_scores)

if __name__ == '__main__':
    app.debug = True
    app.run()
