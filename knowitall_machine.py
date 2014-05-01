


print("Hello Folks! Let's get the KnowItAll Machine started")

import json
import requests

####### Helper methods ########

def download_storyline(storyline):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/storylines/graphs?uri=http://www.bbc.co.uk/things/" + storyline + "&apikey=1XkrNHCERmZnDx4G2AdSsL3gtP9hx0hP"
	print(uri)
	res = requests.get(uri)
	s = json.loads(res.content.decode('utf-8'))
	print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
	return(s)


def download_stories_from_topic(topic):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/things?tag=http://dbpedia.org/resource/" + topic + "&class=http://www.bbc.co.uk/ontologies/creativework/NewsItem&limit=10&after=2014-04-01&apikey=1XkrNHCERmZnDx4G2AdSsL3gtP9hx0hP"
	res = requests.get(uri)
	s = json.loads(res.content.decode('utf-8'))
	print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
	return(s)

####### Actual methods ########


def find_topics_from_storyline(storyline):
	s = download_storyline(storyline)
	topics = s['@graph'][0]['topic']
	#print topics
	return topics

def find_stories_from_topic(topic):
	s = download_stories_from_topic(topic)
	mystories = [];
	for piece in s:
		if piece['type']=='http://www.bbc.co.uk/ontologies/creativework/NewsItem':
			story = {'title': piece['title'], 'product':piece['product'], 'uri':piece['uri'], 'date':piece['date'], 'desc':piece['desc']}
			mystories.append(story);
	#print(mystories)
	return mystories

def find_number_of_stories_from_topic(topic):
	s = download_stories_from_topic(topic)
	number_of_stories = 0;
	for piece in s:
		if piece['type']=='http://www.bbc.co.uk/ontologies/creativework/NewsItem':
			number_of_stories+=1
	#print(number_of_stories)
	return number_of_stories


def find_number_of_stories(storyline):
	s = download_storyline(storyline)
	title = s['@graph'][0]['title'] 
	print(title)

	number_of_stories = 0;
	number_of_chapters = 0;

	all_pieces = s['@graph']
	#all_pieces.pop(0)
	for piece in all_pieces:

		if piece['@type']=='Event':
			print('Event found')
			print(piece['preferredLabel'])
			number_of_chapters+=1;
			sub_pieces = piece['taggedOn'];
			for sub_piece in sub_pieces['@set']:
				#print(sub_piece)
				number_of_stories+=1;
				print(number_of_stories)

	print(number_of_stories)
	print(number_of_chapters)
	return number_of_stories

#find_number_of_stories("29199865-deee-47ad-9079-7276170003a5")
get_number_of_stories_from_topic("Scotland")





#def find_related_stories(storyline):

#def find_related_stories(topic):


#def find_total_stories(topic):


#


	
# def get_storyline_progress(user_id, storyline):
	
	# returns progress for a user based on story line

#def get_storyline_progress(user_id, topic):
	
