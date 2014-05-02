


function get_percentage_read_of_storyline(storyline,pieces_read){

	return 100*(pieces_read/find_number_of_stories_from_storyline(storyline));

}

function get_percentage_read_of_topic(topic,pieces_read){

	return 100*(pieces_read/find_number_of_stories_from_topic(topic));

}


// Much cooler way of getting percentage read and percentage increase..
function get_percentage_of_words_read_of_topic(topic,pieces_read){

	words_read = 0;

	for (piece in pieces_read){

		words_read = words_read + count_words(piece);

	}

	all_pieces_in_topic = find_stories_from_topic(topic);
	total_words = 0

	for (piece in all_pieces_in_topic){

		total_words = total_words + count_words(piece['uri'])

	}


	return 100*(words_read/total_words);

}

// Much cooler way of getting percentage read and percentage increase..
function get_percentage_of_words_read_of_storyline(storyline,pieces_read){

	words_read = 0;

	for (piece in pieces_read){

		words_read = words_read + count_words(piece);

	}

	all_pieces_in_topic = find_stories_from_storyline(storyline);
	total_words = 0

	for (piece in all_pieces_in_topic){

		total_words = total_words + count_words(piece['uri'])

	}


	return 100*(words_read/total_words);
}


function get_reading_speed(start_time,end_time,article_url){

	//start_time = new Date('2011/10/09 12:00')
	//end_time = new Date('2011/10/09 00:00')

	var diff = Math.abs(start_time - end_time);
	var minutes = Math.floor((diff/1000)/60);

	return count_words(article_url)/minutes;

}


function is_valid_read(start_time,end_time,article_url){

	is_valid_read = true;

	if get_reading_speed(start_time,end_time,article_url)<150 || get_reading_speed(start_time,end_time,article_url)>250{

		is_valid_read = false;

	}

	return is_valid_read
}