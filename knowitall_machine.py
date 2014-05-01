


print("Hello Folks! Let's get the KnowItAll Machine started")

import json
import requests

def find_total_stories(storyline):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/storylines/graphs?uri=http://www.bbc.co.uk/things/" + storyline + "&apikey=1XkrNHCERmZnDx4G2AdSsL3gtP9hx0hP"
	print(uri)
	res = requests.get(uri)
	s = json.loads(res.content.decode('utf-8'))
	print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
	return(s)


def find_related_stories(storyline):

	s = find_total_stories(storyline)
	print(s['@graph'][0]['@type'])


find_related_stories("29199865-deee-47ad-9079-7276170003a5")


#def find_related_stories(storyline):

#def find_related_stories(topic):


#def find_total_stories(topic):


#


	
# def get_storyline_progress(user_id, storyline):
	
	# returns progress for a user based on story line

#def get_storyline_progress(user_id, topic):
	
