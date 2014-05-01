# KnowItAll Basic REST API

#import knowitall_machine
import os
from flask import Flask
from flask import jsonify

app = Flask(__name__)

# Main endpoint, returns article data.

@app.route("/<url>")
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
      app.run(host="0.0.0.0",  debug = False)
