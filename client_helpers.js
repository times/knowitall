



function get_percentage_read_of_storyline(storyline,pieces_read){

	return pieces_read/find_number_of_stories_from_storyline(storyline);

}

function get_percentage_read_of_topic(topic,pieces_read){

	return pieces_read/find_number_of_stories_from_topic(topic);

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