var currentVideoId = -1;
var currentSection = 'newest'; //where the song that is playing is
var pageType = 'newest'; //where the user is
var timeFrame = 'alltime';
var search = '';

function updatePage( _pageNumber, _pageType )
{
	if( _pageType == 0 )
	{
		_pageType = 'newest';
	}
	pageType = _pageType;
	document.getElementById( 'arrow' ).className = _pageType + '_arrow';
	if( _pageType == 'search' )
	{
		search = document.getElementById( 'searchbar' ).value;
		document.getElementById( 'searchedterm' ).innerHTML = search;
		document.getElementById( 'searchresults' ).style.height = '40px';
	}
	else
	{
		document.getElementById( 'searchresults' ).style.height = '0px';
	}

	var httpPagebox;

	if( window.XMLHttpRequest )
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		httpPagebox = new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		httpPagebox = new ActiveXObject( 'Microsoft.XMLHTTP' );
	}

	var url = '/pagebox/' + _pageType + '/' + _pageNumber + '/';
	var params =	'time_frame=' + escape(timeFrame) +
					'&search=' + escape(search);
	httpPagebox.open( 'POST', url, true );

	//Send the proper header information along with the request
	httpPagebox.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	httpPagebox.onreadystatechange = function()
	{
		if( httpPagebox.readyState == 4 && httpPagebox.status == 200 )
		{
			//fill the 7 divs with the correct page numbers
			document.getElementById( 'pagebox_upper' ).innerHTML = httpPagebox.responseText;
			document.getElementById( 'pagebox_lower' ).innerHTML = httpPagebox.responseText;
			if( document.getElementById( 'pagebox_lower' ).getElementsByClassName( 'timefilter' )[0] != null )
			{
				document.getElementById( 'pagebox_lower' ).getElementsByClassName( 'timefilter' )[0].innerHTML = '';
			}
			update_time_frame( timeFrame, _pageType );
		}
	}

	httpPagebox.send( params );

	var httpTrackbox;

	if( window.XMLHttpRequest )
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		httpTrackbox = new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		httpTrackbox = new ActiveXObject( 'Microsoft.XMLHTTP' );
	}

	var url = '/' + _pageType + '/' + _pageNumber + '/';
	var params =	'lvVideoId=' + escape(currentVideoId) +
					'&currentSection=' + escape(currentSection) +
					'&time_frame=' + escape(timeFrame) +
					'&search=' + escape(search);
	httpTrackbox.open( 'POST', url, true );

	//Send the proper header information along with the request
	httpTrackbox.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	httpTrackbox.onreadystatechange = function()
	{
		if( httpTrackbox.readyState == 4 && httpTrackbox.status == 200 )
		{
			document.getElementById( 'trackbox' ).innerHTML = httpTrackbox.responseText;
		}
	}

	httpTrackbox.send( params );
}

function hit_like( _lv_video_id, _plus_id, _num_likes_id )
{
	var http;
	
	if( window.XMLHttpRequest )
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		http = new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		http = new ActiveXObject( 'Microsoft.XMLHTTP' );
	}
	
	var url = '/like/' + _lv_video_id + '/';
	var params = '';
	http.open( 'POST', url, true );

	//Send the proper header information along with the request
	http.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	http.onreadystatechange = function()
	{
		if( http.readyState == 4 && http.status == 200 )
		{
			//set the className to the correct value
			document.getElementById( _plus_id ).className = http.responseText;
			if( _num_likes_id != undefined ) {
				if( http.responseText == 'heart' ) {
					document.getElementById( _num_likes_id ).innerHTML = Number( document.getElementById( _num_likes_id ).innerHTML ) + 1;
				} else {
					document.getElementById( _num_likes_id ).innerHTML = Number( document.getElementById( _num_likes_id ).innerHTML ) - 1;
				}
			} else {//this is a trackinfo call and we should update the trackbox song if it exists
				var posts = document.getElementsByClassName('post_title');
				for( var i = 0; i < posts.length; i++ ) {
					if( posts[i].innerHTML == document.getElementById( 'title_big' ).innerHTML ) {
						var plus = get_nextsibling(get_firstchild(get_nextsibling(get_nextsibling(posts[i]))));
						plus.className = http.responseText;
						num_likes = get_nextsibling(plus);
						if( http.responseText == 'heart' ) {
							num_likes.innerHTML = Number( num_likes.innerHTML ) + 1;
						} else {
							num_likes.innerHTML = Number( num_likes.innerHTML ) - 1;
						}
					}
				}
			}
		}
	}

	http.send( params );
}

function post_to_facebook( _id )
{
	var http;
	
	if( window.XMLHttpRequest )
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		http = new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		http = new ActiveXObject( 'Microsoft.XMLHTTP' );
	}
	
	var url = 'ajax/facebook_feed_response.php';
	var params = 'lvVideoId=' + escape(_id);
	http.open( 'POST', url, true );

	//Send the proper header information along with the request
	http.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	http.onreadystatechange = function()
	{
		if( http.readyState == 4 && http.status == 200 )
		{
			//confirm sent
		}
	}

	http.send( params );
}

function generate_trackinfo( _title, _channel, _upload_date_text, _watch_page_url, _lv_video_id )
{
	var http;
	
	if( window.XMLHttpRequest )
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		http = new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		http = new ActiveXObject( 'Microsoft.XMLHTTP' );
	}
	
	
	var url = '/trackinfo/'; //TODO send the lv_video_id in the url, then get rid of all these params
	var params =	'title=' + escape(_title) + '&channel=' + escape(_channel) + '&upload_date_text=' + escape(_upload_date_text) + '&watch_page_url=' + escape(_watch_page_url) + '&lv_video_id=' + escape(_lv_video_id);
	http.open( 'POST', url, true );

	//Send the proper header information along with the request
	http.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	http.onreadystatechange = function()
	{
		if( http.readyState == 4 && http.status == 200 )
		{
			document.getElementById( 'trackinfo' ).innerHTML = http.responseText;
			document.getElementById( 'trackinfo' ).style.visibility = 'visible';
			
			document.getElementById( 'progress' ).onclick = change_progress;
			document.getElementById( 'playpause' ).onclick = play_pause;
		}
	}

	http.send( params );
}

function change_video( _url, _watchPageUrl, _videoId, _title, _channel, _uploadDateText, _section, _lv_video_id, _postType )
{
	if( _postType == 'post' || _postType == 'featured' )
	{
		currentSection = _section;
		currentVideoId = _lv_video_id;
		var elements = document.getElementsByClassName( 'nowplaying' );
		for( var i = 0; i < elements.length; i++ )
		{
			if( elements[i].id == "track_1" && currentSection == 'newest' && _section == 'newest' )
			{
				elements[i].setAttribute( 'class', 'featured' );
			}
			else
			{
				elements[i].setAttribute( 'class', 'post' );
			}
		}
		player.loadVideoById( _videoId, 0, 'large' );
		generate_trackinfo( _title, _channel, _uploadDateText, _watchPageUrl, _lv_video_id );
	}
}

function update_time_frame( _timeFrame, _pageType )
{
	if( _pageType == 'popular' )
	{
		timeFrame = _timeFrame;
		if( _timeFrame == 'month' )
		{
			document.getElementById( 'pop_alltime' ).className = 'btn';
			document.getElementById( 'pop_day' ).className = 'btn';
			document.getElementById( 'pop_week' ).className = 'btn';
			document.getElementById( 'pop_month' ).className = 'btn_x';
		}
		else if( _timeFrame == 'week' )
		{
			document.getElementById( 'pop_alltime' ).className = 'btn';
			document.getElementById( 'pop_day' ).className = 'btn';
			document.getElementById( 'pop_week' ).className = 'btn_x';
			document.getElementById( 'pop_month' ).className = 'btn';
		}
		else if( _timeFrame == 'day' )
		{
			document.getElementById( 'pop_alltime' ).className = 'btn';
			document.getElementById( 'pop_day' ).className = 'btn_x';
			document.getElementById( 'pop_week' ).className = 'btn';
			document.getElementById( 'pop_month' ).className = 'btn';
		}
		else if( _timeFrame == 'alltime' )
		{
			document.getElementById( 'pop_alltime' ).className = 'btn_x';
			document.getElementById( 'pop_day' ).className = 'btn';
			document.getElementById( 'pop_week' ).className = 'btn';
			document.getElementById( 'pop_month' ).className = 'btn';
		}
	}
}

function submitSearch( _e )
{
	if( _e.keyCode == 13 )
	{
		document.getElementById( 'searchbutton' ).click();
	}
}

function get_nextsibling( n )
{
	x = n.nextSibling;
	while( x.nodeType != 1 )
	{
		x = x.nextSibling;
	}
	return x;
}

function get_firstchild( n )
{
	x = n.firstChild;
	while( x.nodeType != 1 )
	{
		x = x.nextSibling;
	}
	return x;
}

function init()
{
	updatePage( 1, 0 );
}

window.onload = init;