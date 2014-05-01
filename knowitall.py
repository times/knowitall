print("Hello Folks! Let's get the KnowItAll Machine started")

import json
import requests

####### Helper methods ########

def download_storyline(storyline):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/storylines/graphs?uri=" + storyline + "&apikey=1XkrNHCERmZnDx4G2AdSsL3gtP9hx0hP"
	#print(uri)
	res = requests.get(uri)
	s = json.loads(res.content.decode('utf-8'))
	#print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
	return(s)


def download_stories_from_topic(topic):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/things?tag=http://dbpedia.org/resource/" + topic + "&class=http://www.bbc.co.uk/ontologies/creativework/NewsItem&limit=10&after=2014-04-01&apikey=1XkrNHCERmZnDx4G2AdSsL3gtP9hx0hP"
	res = requests.get(uri)
	s = json.loads(res.content.decode('utf-8'))
	#print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
	return(s)

####### Actual methods ########

def find_details_from_uri(uri):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/creative-works?uri=" + uri + "&apikey=1XkrNHCERmZnDx4G2AdSsL3gtP9hx0hP"
	print uri
	res = requests.get(uri)
	s = json.loads(res.content.decode('utf-8'))
	details = s['@graph'][0]
	subject = details['subject']
	title = details['title']
	desc = details['description']
	date = details['dateCreated']
	storyline_id = ''
	for detail in details['tag']['@set']:

		if detail['@type']=='Storyline':
			storyline_id=detail['@id']

	details = {'title':title, 'subject': subject, 'desc':desc, 'date':date,'storyline_id':storyline_id}
	return(details)

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
			story = {'title': piece['title'], 'product':piece['product'], 'uri':piece['uri'], 'date':piece['date'], 'desc':piece['desc'], 'parent':topic, 'parent_type':'topic'}
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


def find_number_of_stories_from_storyline(storyline):
	s = download_storyline(storyline)
	title = s['@graph'][0]['title']
	#print(title)

	number_of_stories = 0;
	number_of_chapters = 0;

	all_pieces = s['@graph']
	children_pieces = s['@graph'][0]['taggedOn'];

	for child_piece in children_pieces['@set']:
		number_of_stories+=1;

	for piece in all_pieces:
		if piece['@type']=='Event':
			#print('Event found')
			#print(piece['preferredLabel'])
			number_of_chapters+=1;
			sub_pieces = piece['taggedOn'];
			for sub_piece in sub_pieces['@set']:
				#print(sub_piece)
				number_of_stories+=1;
				#print(number_of_stories)

	return number_of_stories

def find_stories_from_storyline(storyline):
	s = download_storyline(storyline)
	title = s['@graph'][0]['title']
	print(title)

	mystories = [];
	all_pieces = s['@graph']

	children_pieces = s['@graph'][0]['taggedOn'];
	for child_piece in children_pieces['@set']:
		story = {'title': child_piece['title'], 'product':child_piece['product'], 'uri':child_piece['@id'], 'date':child_piece['dateCreated'], 'desc':child_piece['description'],'parent':storyline,'parent_type':'storyline'}
		mystories.append(story);

	for piece in all_pieces:

		if piece['@type']=='Event':
			sub_pieces = piece['taggedOn'];
			for sub_piece in sub_pieces['@set']:
				story = {'title': sub_piece['title'], 'product':sub_piece['product'], 'uri':sub_piece['@id'], 'date':sub_piece['dateCreated'], 'desc':sub_piece['description'],'parent':piece['preferredLabel'],'parent_type':'chapter'}
				mystories.append(story);
				#print(story)

	return mystories


###### percentage functions ######

def get_percentage_of_storyline(storyline,pieces_read):

	return len(pieces_read)/find_number_of_stories_from_storyline('storyline')



def get_percentage_of_topic(topic,pieces_read):

	return len(pieces_read)/find_number_of_stories_from_topic('topic')




####### test #######

#print(find_details_from_uri('http://www.bbc.co.uk/news/uk-scotland-13323587'))
#print(find_number_of_stories_from_topic("David_Cameron"))

#print(find_number_of_stories_from_storyline("29199865-deee-47ad-9079-7276170003a5"))
#print(find_topics_from_storyline("29199865-deee-47ad-9079-7276170003a5"))
