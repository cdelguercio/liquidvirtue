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
	document.getElementById( 'arrow' ).className = _pageType;
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

	var url = '/' + _pageType + '/' + _pageNumber + '/';
	/*var params =	'pageNumber=' + escape(_pageNumber) +
					'&pageType=' + escape(_pageType) +
					'&user=' + escape(facebook_id) +
					'&timeFrame=' + escape(timeFrame) +
					'&search=' + escape(search);*/
	var params = '';
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

	var url = '/videos/' + currentVideoId + '/';
	/*var params =	'pageNumber=' + escape(_pageNumber) +
					'&user=' + escape(facebook_id) +
					'&pageType=' + escape(_pageType) +
					'&lvVideoId=' + escape(currentVideoId) +
					'&currentSection=' + escape(currentSection) +
					'&timeFrame=' + escape(timeFrame) +
					'&search=' + escape(search);*/
	var params = '';
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

function hit_like( _title, _id )
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
	
	var url = 'ajax/like_response.php';
	var params = 'title=' + escape(_title) + '&user=' + escape(facebook_id);
	http.open( 'POST', url, true );

	//Send the proper header information along with the request
	http.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	http.onreadystatechange = function()
	{
		if( http.readyState == 4 && http.status == 200 )
		{
			//set the className to the correct value
			document.getElementById( _id ).className = http.responseText;
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

function generate_trackinfo( _title, _channel, _uploadDateText, _watchPageUrl, _id )
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
	
	
	var url = 'ajax/trackinfo_response.php';
	var params =	'title=' + escape(_title) +
					'&user=' + escape(facebook_id);
	http.open( 'POST', url, true );

	//Send the proper header information along with the request
	http.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	http.onreadystatechange = function()
	{
		if( http.readyState == 4 && http.status == 200 )
		{
			document.getElementById( "trackinfo" ).innerHTML = '<button id="playpause" class="pause"></button><button id="progress" class="progressBar"><div id="elapsed" class="elapsed"></div></button>'
			+ '<h1>' + _title + '</h1><p><b onclick="window.open(\'http://www.youtube.com/' + _channel + '\')">' + _channel + '</b> (' + _uploadDateText + ')<br />'
			+ '<div id="viewpost" class="viewpost" onclick="window.open(\'' + _watchPageUrl + '\')"><p>View post on youtube</p></div>'
			+ '<div class="btnspace"></div>'
			+ '<div id="sharesong" class="sharesong" onclick="window.open(\'http://www.facebook.com/sharer.php?u=http%3A%2F%2Fwww.liquidvirtue.com%2F%3Fid%3D' + escape(_id) + '&t=The%20newest%20drum%20and%20bass%20tracks\')"><p>Share this track on facebook</p></div>'
			//+ '<div id="sharesong" class="sharesong" onclick="post_to_facebook( ' + _id + ' )"><p>Share this track on facebook</p></div>'
			+ '<div class="btnspace"></div>'
			+ '<div id="like_big"' + http.responseText + '</p></div>';
			document.getElementById( 'trackinfo' ).style.visibility = 'visible';
			
			document.getElementById( 'progress' ).onclick = change_progress;
			document.getElementById( 'playpause' ).onclick = play_pause;
		}
	}

	http.send( params );
}

function change_video( _url, _watchPageUrl, _videoId, _title, _channel, _uploadDateText, _section, _id, _postType )
{
	if( _postType == 'post' || _postType == 'featured' )
	{
		currentSection = _section;
		currentVideoId = _id;
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
		generate_trackinfo( _title, _channel, _uploadDateText, _watchPageUrl, _id );
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

function init()
{
	updatePage( 1, 0 );
}

window.onload = init;