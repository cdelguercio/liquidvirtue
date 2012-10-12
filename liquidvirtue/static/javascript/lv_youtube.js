var undefined;
var player;
var interval;

var tag = document.createElement( 'script' );
tag.src = 'http://www.youtube.com/player_api';
var firstScriptTag = document.getElementsByTagName( 'script' )[0];
firstScriptTag.parentNode.insertBefore( tag, firstScriptTag );

function onYouTubePlayerAPIReady() {
	player = new YT.Player( 'video', {
		height: '200', //old = 160, 16:9 = 135
		width: '300', //old = 240, 16:9 = 240
		videoId: '',
		playerVars: {
			'controls': 0,
			'origin': 'www.liquidvirtue.com'
		},
		events: {
			'onReady': onPlayerReady,
			'onStateChange': onPlayerStateChange,
			'onError': onPlayerError
		}
	} );
}

function change_progress( e )
{
	// When a click occurs on the progress bar, seek to the
	// appropriate moment of the video.
	
	var obj = document.getElementById( 'progress' );
	var curleft = 0;
	if( obj.offsetParent )
	{
		do
		{
			curleft += obj.offsetLeft;
		} while( obj = obj.offsetParent );
	}
	
	var elapsedLength = 215
	var ratio = ( e.pageX - curleft ) / elapsedLength;
	if( ratio < 0 )
	{
		ratio = 0;
	}
	if( ratio > 1 )
	{
		ratio = 1;
	}
	
	document.getElementById( 'elapsed' ).style.width = ratio * 100 + '%';
	player.seekTo( Math.round( player.getDuration() * ratio ), true );
	return false; //something about causing a refresh unneccessarily
}

function play_pause( e )
{
	if( document.getElementById( 'playpause' ).className == 'pause' )
	{
		//document.getElementById( 'playpause' ).className = 'play';
		player.pauseVideo();
	}
	else if( document.getElementById( 'playpause' ).className == 'play' )
	{
		//document.getElementById( 'playpause' ).className = 'pause';
		player.playVideo();
	}
	return false;
}

function onPlayerReady( event )
{
	if( lv_autoplay_id != undefined && youtube_autoplay_id != undefined )
	{
		player.loadVideoById( youtube_autoplay_id, 0, 'large' );
		generate_trackinfo( lv_autoplay_id );
	}
}

function htmlEncode( s )
{
	var el = document.createElement( 'div' );
	el.innerText = el.textContent = s;
	s = el.innerHTML;
	delete el;
	return s;
}

function playNext()
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

	var url = '/get_next/';
	var params = 'currentVideoId=' + escape(currentVideoId) + '&currentSection=' + escape(currentSection) + '&time_frame=' + timeFrame + '&search=' + search;
	http.open( 'POST', url, true );

	//Send the proper header information along with the request
	http.setRequestHeader( 'Content-type', 'application/x-www-form-urlencoded' );

	http.onreadystatechange = function()
	{
		if( http.readyState == 4 && http.status == 200 )
		{
			var elements = document.getElementsByClassName( 'nowplaying' );
			for( var i = 0; i < elements.length; i++ )
			{
				if( elements[i].id == "track_1" && currentSection == 'newest' && pageType == 'newest' )
				{
					elements[i].setAttribute( 'class', 'post' );
					//elements[i].setAttribute( 'class', 'featured' );
				}
				else
				{
					elements[i].setAttribute( 'class', 'post' );
				}
			}
			var items = http.responseText.split('|');
			currentVideoId = items[0];
			if( currentVideoId && (currentVideoId != "") )
			{
				player.loadVideoById( items[2], 0, 'large' );

				generate_trackinfo( items[0] );
				
				var posts = document.getElementsByClassName( 'post' );
				for( var i in posts )
				{
					if( get_firstchild(posts[i]).innerHTML == items[1] || get_firstchild(posts[i]).innerHTML == htmlEncode(items[1]) )
					{
						posts[i].className = 'nowplaying';
						break;
					}
				}
			}
			else
			{
				alert( 'Error: Ran out of songs to play!' );
			}
		}
	}

	http.send( params );
}

function onPlayerStateChange( event ) {
	if ( event.data == YT.PlayerState.ENDED ) {
		playNext();
	}
	else if ( event.data == YT.PlayerState.PLAYING ) {
		document.getElementById( 'playpause' ).className = 'pause';
		interval = window.setInterval( function() {
			document.getElementById( 'elapsed' ).style.width = ( player.getCurrentTime() / player.getDuration() ) * 100 + '%';
		}, 250 );
	}
	else if ( event.data == YT.PlayerState.PAUSED ) {
		document.getElementById( 'playpause' ).className = 'play';
		window.clearInterval( interval );
	}
}

function onPlayerError( event )
{
	playNext();
}