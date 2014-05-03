# KnowItAll Basic REST API
import pprint
pp = pprint.PrettyPrinter(indent=4)

from knowitall import *
import os
from flask import *
from cors import crossdomain

app = Flask(__name__)

cache = []

def in_cache(url):
  global cache
  for item in cache:
    if item["url"] == url:
      return item
  return False

# Main endpoint, returns article data.

@app.route("/favicon.ico")
def missing():
    return '404'

@app.route('/', defaults={'url': ''})
@app.route('/<path:url>')
@crossdomain(origin='*')
def return_article_details(url):
    story_topics = False
    related_stories = False
    if in_cache(url): 
      print "in cache"
      cached = in_cache(url)
      article_details = cached["data"]
    else:
      print "not in cache"
      article_details = find_details_from_uri(url)
      if article_details:
        global cache
        cache.append({"url": url, "data": article_details})

    if article_details:
      storyline = article_details['storyline_id']
      if storyline:
        storyline_blob = download_storyline(storyline)
        related_stories = find_stories_from_storyline(storyline_blob)
        story_topics = find_topics_from_storyline(storyline_blob)
      else:
        print "No storyline"
    else:
      print "No article details"

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
