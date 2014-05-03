


// pieces_read is an array of urls
function get_percentage_of_words_read_of_topic(topic,pieces_read){

	var words_read = 0;

	for (piece in pieces_read){

		words_read = words_read + count_words(piece);

	}

	var all_pieces_in_topic = find_stories_from_topic(topic);
	var total_words = 0

	for (piece in all_pieces_in_topic){

		total_words = total_words + count_words(piece['uri'])

	}


	return 100*(words_read/total_words);

}

// pieces_read is an array of urls
function get_percentage_of_words_read_of_storyline(storyline,pieces_read){

	var words_read = 0;

	for (piece in pieces_read){

		words_read = words_read + count_words(piece);

	}

	var all_pieces_in_topic = find_stories_from_storyline(storyline);
	var total_words = 0

	for (piece in all_pieces_in_topic){

		total_words = total_words + count_words(piece['uri'])

	}


	return 100*(words_read/total_words);
}



// pieces_read is an array of urls
function get_percentage_read_of_storyline(storyline,pieces_read){

	return 100*(pieces_read/find_number_of_stories_from_storyline(storyline));

}



// pieces_read is an array of urls
function get_percentage_read_of_topic(topic,pieces_read){

	return 100*(pieces_read/find_number_of_stories_from_topic(topic));

}

// gets users reading speed
function get_reading_speed(start_time,end_time,article_url){

	//start_time = new Date('2011/10/09 12:00')
	//end_time = new Date('2011/10/09 00:00')

	var diff = Math.abs(start_time - end_time);
	var minutes = Math.floor((diff/1000)/60);

	return count_words(article_url)/minutes;

}

function get_personal_avg_reading_speed(piece_read,total_time_spent){

}

function get_remaining_reading_time(piece_read,storyline){

}

// Check if the reader actually read the piece
// use Date objects
function is_valid_read(start_time,end_time,article_url){

	var is_valid_read = true;

	if get_reading_speed(start_time,end_time,article_url)<150 || get_reading_speed(start_time,end_time,article_url)>250{

		is_valid_read = false;

	}

	return is_valid_read
}



function check_if_a_piece_has_already_been_read(pieces_read,article_url){

	var found = 0;

	for (piece in pieces_read){
		if (article_url==piece){
			found = 1;
		}
	}

}


// Calculate the percentage increase of a storyline
// pieces read is an array of urls
function calculate_percentage_increase_for_a_story(pieces_read,storyline,article_url){

	var increase = 0;

	if (check_if_a_piece_has_already_been_read(pieces_read,article_url)==0){ // if it hasn't been already read..

		var percentage_before = get_percentage_of_words_read_of_storyline(storyline,pieces_read);
		var pieces_read_including_new_piece = pieces_read.push(article_url);
	    var percentage_after = get_percentage_of_words_read_of_storyline(storyline,pieces_read_including_new_piece);
	    
	    increase = percentage_after-percentage_before;

	} 

	return increase;
}

function calculate_story_age_in_hrs(story){
	var start_time = Date.now();
	var age_in_ms = start_time - story.date;
	
	return age_in_ms/(1000*60*60)
}

// Refined reccomendation system: it returns stories that you havent read, sorted by a combined metric based on how old is a story and how much it increases your percentage!
function suggest_me_stories(article_url,storyline,related_stories,story_topics,pieces_read,sorting_method){

	related_stories_copy = related_stories;
	var index = -1;

	for (story in related_stories_copy){

		if (check_if_a_piece_has_already_been_read(pieces_read,story)==1){ // if it has been already read..
			index = related_stories.indexOf(story);
			if (index > -1) {
			    related_stories.splice(index, 1);
			}
		}

	}


	for (story in related_stories){

		story['Percentage_increase'] = calculate_percentage_increase_for_a_story(pieces_read,storyline,article_url);
		story['Age_in_Hours'] = calculate_story_age_in_hrs(story);

		if (sorting_method=='Increase'){
			story['Sorting_score'] = -story['Age_in_Hours']+story['Percentage_increase'];
		}
		if (sorting_method=='Combined'){
			story['Sorting_score'] = -story['Age_in_Hours'];
		}

	}

	related_stories.sort(function(a,b) { return parseFloat(a.Sorting_score) - parseFloat(b.Sorting_score) } );
	
	return related_stories;
	 
}
