# KnowItAll Basic REST API

#import knowitall_machine
import os
from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.debug = True

# Main endpoint, returns article data.

@app.route("/<url>")
def return_article_details(url):
    storyline = find_storyline(url)
    related_stories = find_related_stories(storyline)
    story_topics = find_topics(storyline)

    response = {
      "topics": [],
      "related": []
    }

    return jsonify(**response)

if __name__ == "__main__":
    if os.getenv('KNOWITALL_ENV', "dev") == "dev":
      app.run(host="127.0.0.1",  debug = True)
    else:
      app.run(host="0.0.0.0",  debug = False)
