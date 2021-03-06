
api_key = "c4Eybj69ezJsWwAKZ1I8JxtvyVqqf9EH"

print("Hello Folks! Let's get the KnowItAll Machine started")

import json
import requests
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)
####### Helper methods ########

def download_storyline(storyline):
	if storyline == "http://www.bbc.co.uk/things/67cfb3fa-a263-499a-9193-78a1c1b25f29":
		print "debug"
		storyline_debug = open("./debug_storyline.json", "r")
		storyline_debug_content = storyline.read() 
		return json.loads(storyline_debug_content.decode("utf-8"))


	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/storylines/graphs?uri=" + storyline + "&apikey=" + api_key
	#print(uri)
	try:
		res = requests.get(uri, timeout=1)
		try:
			s = json.loads(res.content.decode('utf-8'))
			return(s)
		except:
			print "Failure on storyline"
			return False
			#print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
	except:
		print "Storyline connection timeout"
		return False


def download_stories_from_topic(topic):
	uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/things?tag=http://dbpedia.org/resource/" + topic + "&class=http://www.bbc.co.uk/ontologies/creativework/NewsItem&limit=1&after=2014-04-01&apikey=" + api_key
	try:
		res = requests.get(uri, timeout=1)
		try:
			s = json.loads(res.content.decode('utf-8'))
		except:
			print "Failure on topics"
			return False
		#print(json.dumps(s, sort_keys=True,indent=4, separators=(',', ': ')))
		return(s)
	except:
		print "timeout on getting story from topic"
		return False

####### Actual methods ########

def find_details_from_uri(uri):
	print uri
	if uri == "http://www.bbc.co.uk/news/business-16548644":
		print "debug details"
		res = open("./debug_article.json")
		details = res.read()
		try:
			s = json.loads(details.decode('utf-8'))
		except:
			print "Failure on details"
			return False
	else:
		uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/creative-works?uri=" + uri + "&apikey=" + api_key
		try:
			res = requests.get(uri, timeout=5)
			try:
				s = json.loads(res.content.decode('utf-8'))
			except:
				print "Failure on details"
				return False
		except:
			print "timeout on finding details"
			return False

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


def find_topics_from_storyline(storyline_blob):
	s = storyline_blob
	if s != False:
		topics = s['@graph'][0]['topic']
		#print topics
		return topics
	else:
		return False

def find_stories_from_topic(topic):
	s = download_stories_from_topic(topic)
	if s != False:
		mystories = [];
		for piece in s:
			if piece['type']=='http://www.bbc.co.uk/ontologies/creativework/NewsItem':
				story = {'title': piece['title'], 'product':piece['product'], 'uri':piece['uri'], 'date':piece['date'], 'desc':piece['desc'], 'parent':topic, 'parent_type':'topic'}
				mystories.append(story);
		#print(mystories)
		return mystories
	else:
		return False

def find_number_of_stories_from_topic(topic):
	s = download_stories_from_topic(topic)
	if s != False:
		number_of_stories = 0;
		for piece in s:
			if piece['type']=='http://www.bbc.co.uk/ontologies/creativework/NewsItem':
				number_of_stories+=1
		#print(number_of_stories)
		return number_of_stories
	else:
		return 0

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

def find_stories_from_storyline(storyline_blob):
	s = storyline_blob
	storyline = storyline_blob["@graph"][0]["@id"]

	if s:
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
	else:
		return False


def count_words(url):
	try:
		uri = "http://data.bbc.co.uk/v1/bbcrd-newslabs/creative-works?uri=" + url + "&apikey=" + api_key
		res = requests.get(uri, timeout=1)
		try:
			s = json.loads(res.content.decode('utf-8'))
		except:
			return False

		#print(s)
		details = s['@graph'][0]
		article_id = details['identifier']

		uri = "http://data.bbc.co.uk/bbcrd-juicer/articles/" + article_id + ".json?apikey=" + api_key
		res = requests.get(uri, timeout=1)
		try:
			s = json.loads(res.content.decode('utf-8'))
		except:
			print "failure on word count"
			return False
		body = s['article']['body']
		#splitted = body.split()
		splitted = re.findall(r"[\w']+", body)
		#print(splitted)
		return len(splitted)
	except:
		print "timeout on wordcount"
		return False


####### test #######

#print(find_details_from_uri('http://www.bbc.co.uk/news/uk-scotland-13323587'))
#print(find_number_of_stories_from_topic("David_Cameron"))

#print(find_number_of_stories_from_storyline("29199865-deee-47ad-9079-7276170003a5"))
#print(find_topics_from_storyline("29199865-deee-47ad-9079-7276170003a5"))

#print(count_words('http://www.bbc.co.uk/news/uk-scotland-13323587'))
