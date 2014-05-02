# KnowItAll Basic REST API

from knowitall import *
import os
from flask import *
from cors import crossdomain

app = Flask(__name__)

# Main endpoint, returns article data.

@app.route("/favicon.ico")
def missing():
    return '404'

@app.route('/', defaults={'url': ''})
@app.route('/<path:url>')
@crossdomain(origin='*')
def return_article_details(url):
    article_details = find_details_from_uri(url)
    storyline = article_details['storyline_id']
    related_stories = find_stories_from_storyline(storyline)
    story_topics = find_topics_from_storyline(storyline)

    response = {
      "topics": story_topics,
      "related": related_stories
    }

    return jsonify(**response)

if __name__ == "__main__":
    if os.getenv('KNOWITALL_ENV', "dev") == "dev":
      app.run(host="127.0.0.1",  debug = True)
    else:
      app.run(host="0.0.0.0",  debug = True)
