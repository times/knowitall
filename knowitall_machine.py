


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

def find_topics(storyline):

	s = find_total_stories(storyline)

	topics = s['@graph'][0]['topic']

	return topics


def find_related_stories(storyline):

	s = find_total_stories(storyline)

	topics = s['@graph'][0]['topic']
	type_check = s['@graph'][0]['@type'] 
	title = s['@graph'][0]['title'] 
	
	print(title)
	number_of_stories = 0;

	all_pieces = s['@graph']
	#all_pieces.pop(0)
	for piece in all_pieces:
		if piece['@type']=='StorylineSlot':
			print(piece)
			number_of_stories+=1
			print(number_of_stories)


		if piece['@type']=='Event':
			print('Event found')
			sub_pieces = piece['taggedOn'];
			for sub_piece in sub_pieces['@set']:
				print(sub_piece)
				number_of_stories+=1;
				print(number_of_stories)




	print(number_of_stories)

	#print(s['@graph'][0]['@type'])




find_related_stories("29199865-deee-47ad-9079-7276170003a5")




#def find_related_stories(storyline):

#def find_related_stories(topic):


#def find_total_stories(topic):


#


	
# def get_storyline_progress(user_id, storyline):
	
	# returns progress for a user based on story line

#def get_storyline_progress(user_id, topic):
	
