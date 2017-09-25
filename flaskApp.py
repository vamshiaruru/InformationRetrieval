from search import Searcher
from flask import Flask, render_template, request
import unicodedata
app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/displayResults", methods=['POST'])
def search():
    query = request.form['searchBar']
    query = unicodedata.normalize('NFKD', query).encode('ascii', 'ignore')
    searcher = Searcher(query)
    results = searcher.cosine_score()
    scores = searcher.query_score
    print results
    return render_template("displayResults.html", input_query=query,
                           results=results, scores=scores)

if __name__ == '__main__':
    app.debug = True
    app.run()
