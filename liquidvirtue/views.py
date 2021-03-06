from django.shortcuts import render_to_response, get_object_or_404
from liquidvirtue.models import UserProfile
from liquidvirtue.models import Like
from liquidvirtue.models import Channel
from liquidvirtue.models import Video
from datetime import datetime
import time
from django.template import RequestContext
from itertools import izip
from math import floor
from django.db.models import Q
from django.utils import timezone

def index(request):
	track_initializer = ''
	return render_to_response('index.html', {'track_initializer': track_initializer}, context_instance=RequestContext(request))
		
def index_with_id(request, lv_video_id):
	v = ''
	track_initializer = ''
	if Video.objects.get(pk=lv_video_id):
		video = Video.objects.get(pk=lv_video_id)
		track_initializer = '<script>lv_autoplay_id = ' + lv_video_id + '; youtube_autoplay_id = "' + video.youtube_video_id + '";</script>'
	else:
		track_initializer = ''

	return render_to_response('index.html', {'track_initializer': track_initializer}, context_instance=RequestContext(request))

def get_next(request):
	lv_video_id = request.POST["currentVideoId"]
	page_type = request.POST["currentSection"]
	time_frame = request.POST["time_frame"]
	search = request.POST["search"]
	
	now_time = time.time()
	
	v = Video.objects.get(pk=lv_video_id)
	next_video = ''
	
	if page_type == 'popular':
		if time_frame == 'month':
			if Video.objects.filter(upload_time__gt=(now_time-86400 * 30)).filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time').exists():
				next_video = Video.objects.filter(upload_time__gt=(now_time-86400 * 30)).filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time')[0]
			else: #ran out of videos, play the first one
				next_video = Video.objects.filter(upload_time__gt=(now_time-86400 * 30)).order_by('-num_likes', '-upload_time')[0]
		elif time_frame == 'week':
			if Video.objects.filter(upload_time__gt=(now_time-86400 * 7)).filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time').exists():
				next_video = Video.objects.filter(upload_time__gt=(now_time-86400 * 7)).filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time')[0]
			else: #ran out of videos, play the first one
				next_video = Video.objects.filter(upload_time__gt=(now_time-86400 * 7)).order_by('-num_likes', '-upload_time')[0]
		elif time_frame == 'day':
			if Video.objects.filter(upload_time__gt=(now_time-86400)).filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time').exists():
				next_video = Video.objects.filter(upload_time__gt=(now_time-86400)).filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time')[0]
			else: #ran out of videos, play the first one
				next_video = Video.objects.filter(upload_time__gt=(now_time-86400)).order_by('-num_likes', '-upload_time')[0]
		else: #all_time
			if Video.objects.filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time').exists():
				next_video = Video.objects.filter(Q(upload_time__lt=v.upload_time, num_likes=v.num_likes) | Q(num_likes__lt=v.num_likes)).order_by('-num_likes', '-upload_time')[0]
			else: #ran out of videos, play the first one
				next_video = Video.objects.order_by('-num_likes', '-upload_time')[0]
	elif page_type == 'my_library':
		if Video.objects.filter(like__user__id__exact=request.user.id).filter(upload_time__lt=v.upload_time).order_by('-upload_time').exists():
			next_video = Video.objects.filter(like__user__id__exact=request.user.id).filter(upload_time__lt=v.upload_time).order_by('-upload_time')[0]
		else: #ran out of videos, play the first one
			next_video = Video.objects.filter(like__user__id__exact=request.user.id).order_by('-upload_time')[0]
	elif page_type == 'search':
		if Video.objects.filter(title__icontains=search).filter(upload_time__lt=v.upload_time).order_by('-upload_time').exists():
			next_video = Video.objects.filter(title__icontains=search).filter(upload_time__lt=v.upload_time).order_by('-upload_time')[0]
		else: #ran out of videos, play the first one
			next_video = Video.objects.filter(title__icontains=search).order_by('-upload_time')[0]
	else: #newest
		if Video.objects.filter(upload_time__lt=v.upload_time).order_by('-upload_time').exists():
			next_video = Video.objects.filter(upload_time__lt=v.upload_time).order_by('-upload_time')[0]
		else: #ran out of videos, play the first one
			next_video = Video.objects.order_by('-upload_time')[0]

	lv_video_id = next_video.id
	title = next_video.title
	youtube_video_id = next_video.youtube_video_id

	return render_to_response('get_next.html', {'lv_video_id': lv_video_id, 'title': title, 'youtube_video_id': youtube_video_id})

def like(request, lv_video_id):
	like_status = ''
	if request.user.is_authenticated:
		userprofile = False
		try:
			userprofile = UserProfile.objects.get(pk=request.user.id)
		except UserProfile.DoesNotExist:
			pass
		if userprofile:
			if Like.objects.filter(user=request.user.id).filter(video=lv_video_id).exists():
				v = Video.objects.get(pk=lv_video_id)
				v.num_likes = v.num_likes - 1
				if v.num_likes < 0:
					v.num_likes = 0
				v.save()
				l = Like.objects.filter(user=request.user.id).filter(video=lv_video_id)
				l.delete()
				like_status = 'plus'
			else:
				v = Video.objects.get(pk=lv_video_id)
				v.num_likes = v.num_likes + 1
				v.save()
				l = Like( video=v, user=UserProfile.objects.get(pk=request.user.id) )
				l.save()
				like_status = 'heart'
		
	return render_to_response('like.html', {'like_status': like_status})

def pagebox(request, page_type, page_number):
	time_frame = request.POST["time_frame"]
	search = request.POST["search"]
	num_videos = 0
	now_time = time.time()
	if page_type == 'search':
		num_videos = Video.objects.filter(title__icontains=search).count()
	elif page_type == 'my_library':
		num_videos = Video.objects.filter(like__user__id__exact=request.user.id).count()
	elif page_type == 'popular':
		if time_frame == 'month':
			num_videos = Video.objects.filter(upload_time__gt=(now_time-86400 * 30)).count()
		elif time_frame == 'week':
			num_videos = Video.objects.filter(upload_time__gt=(now_time-86400 * 7)).count()
		elif time_frame == 'day':
			num_videos = Video.objects.filter(upload_time__gt=(now_time-86400)).count()
		else: #all_time
			num_videos = Video.objects.count()
	else:
		num_videos = Video.objects.count()

	max_pages = int( floor( (num_videos - 1) / 17 ) + 1 )
	page_number = int( page_number )

	if page_number > max_pages:
		page_number = max_pages
	if page_number <= 0:
		page_number = 1

	start_page = 0
	end_page = 0
	
	if page_number < 5:
		if max_pages < 7:
			start_page = 1
			end_page = max_pages
		else:
			start_page = 1
			end_page = 7
	else:
		if page_number + 3 <= max_pages:
			start_page = page_number - 3
			end_page = page_number + 3
		else:
			if max_pages - 6 < 1:
				start_page = 1
				end_page = max_pages
			else:
				start_page = max_pages - 6
				end_page = max_pages

	return render_to_response('pagebox.html', {'page_type': page_type, 'page_number': page_number, 'start_page': start_page, 'end_page': end_page + 1}) #end_page + 1 because range is EXCLUSIVE of the stop value

def trackbox_newest(request, page_number):
	lv_video_id = request.POST["lvVideoId"]
	page_type = 'newest'
	page_number = int( page_number )
	num_videos = Video.objects.count()
	max_pages = int( floor( (num_videos - 1) / 17 ) + 1 )
	if page_number > max_pages:
		page_number = max_pages
	if page_number <= 0:
		page_number = 1
	videos = Video.objects.order_by('-upload_time')[(page_number-1)*17:(page_number*17)]
	
	now = timezone.now()
	
	upload_date_texts = []
	class_names = []
	
	for video in videos:
		upload_date_text = get_upload_date_text( video.upload_date, now )
		upload_date_texts.append(upload_date_text)
		if Like.objects.filter(user=request.user.id).filter(video=video.id).exists():
			class_names.append( 'heart' )
		else:
			class_names.append( 'plus' )

	videos_with_metadata = izip(videos, upload_date_texts, class_names)
	
	return render_to_response('trackbox.html', {'videos': videos_with_metadata, 'lv_video_id': lv_video_id, 'page_type': page_type})

def trackbox_popular(request, page_number):
	lv_video_id = request.POST["lvVideoId"]
	time_frame = request.POST["time_frame"]
	page_type = 'popular'
	page_number = int(page_number)
	now_time = time.time()
	num_videos = 0
	if time_frame == 'month':
		num_videos = Video.objects.filter(upload_time__gt=(now_time-86400 * 30)).count()
	elif time_frame == 'week':
		num_videos = Video.objects.filter(upload_time__gt=(now_time-86400 * 7)).count()
	elif time_frame == 'day':
		num_videos = Video.objects.filter(upload_time__gt=(now_time-86400)).count()
	else:
		num_videos = Video.objects.count()
	max_pages = int( floor( (num_videos - 1) / 17 ) + 1 )
	if page_number > max_pages:
		page_number = max_pages
	if page_number <= 0:
		page_number = 1

	videos = []
	if time_frame == 'month':
		videos = Video.objects.filter(upload_time__gt=(now_time-86400 * 30)).order_by('-num_likes', '-upload_time')[(page_number-1)*17:(page_number*17)]
	elif time_frame == 'week':
		videos = Video.objects.filter(upload_time__gt=(now_time-86400 * 7)).order_by('-num_likes', '-upload_time')[(page_number-1)*17:(page_number*17)]
	elif time_frame == 'day':
		videos = Video.objects.filter(upload_time__gt=(now_time-86400)).order_by('-num_likes', '-upload_time')[(page_number-1)*17:(page_number*17)]
	else:
		videos = Video.objects.order_by('-num_likes', '-upload_time')[(page_number-1)*17:(page_number*17)]
	
	now = timezone.now()
	
	upload_date_texts = []
	class_names = []
	
	for video in videos:
		upload_date_text = get_upload_date_text( video.upload_date, now )
		upload_date_texts.append(upload_date_text)
		if Like.objects.filter(user=request.user.id).filter(video=video.id).exists():
			class_names.append( 'heart' )
		else:
			class_names.append( 'plus' )
		
	videos_with_metadata = izip(videos, upload_date_texts, class_names)

	return render_to_response('trackbox.html', {'videos': videos_with_metadata, 'page_type': page_type})
	
def trackbox_my_library(request, page_number):
	#lv_video_id = request.POST["lvVideoId"]
	page_type = 'my_library'
	page_number = int(page_number)
	num_videos = Video.objects.filter(like__user__id__exact=request.user.id).count()
	max_pages = int( floor( (num_videos - 1) / 17 ) + 1 )
	if page_number > max_pages:
		page_number = max_pages
	if page_number <= 0:
		page_number = 1
	videos = Video.objects.filter(like__user__id__exact=request.user.id).order_by('-upload_time')[(page_number-1)*17:(page_number*17)]
	#l = Like.objects.filter(user=request.user.id)
	#videos = l.video_set.order_by('-upload_time')[(page_number-1)*17:(page_number*17)]

	now = timezone.now()

	upload_date_texts = []
	class_names = []
	
	for video in videos:
		upload_date_text = get_upload_date_text( video.upload_date, now )
		upload_date_texts.append(upload_date_text)
		if Like.objects.filter(user=request.user.id).filter(video=video.id).exists():
			class_names.append( 'heart' )
		else:
			class_names.append( 'plus' )
		
	videos_with_metadata = izip(videos, upload_date_texts, class_names)

	return render_to_response('trackbox.html', {'videos': videos_with_metadata, 'page_type': page_type})

def trackbox_search(request, page_number):
	search = request.POST["search"]
	page_type = 'search'
	page_number = int(page_number)
	num_videos = Video.objects.filter(title__icontains=search).count()
	max_pages = int( floor( (num_videos - 1) / 17 ) + 1 )
	if page_number > max_pages:
		page_number = max_pages
	if page_number <= 0:
		page_number = 1
	videos = Video.objects.filter(title__icontains=search).order_by('-upload_time')[(page_number-1)*17:(page_number*17)]

	now = timezone.now()

	upload_date_texts = []
	class_names = []
	
	for video in videos:
		upload_date_text = get_upload_date_text( video.upload_date, now )
		upload_date_texts.append(upload_date_text)
		if Like.objects.filter(user=request.user.id).filter(video=video.id).exists():
			class_names.append( 'heart' )
		else:
			class_names.append( 'plus' )
		
	videos_with_metadata = izip(videos, upload_date_texts, class_names)
	return render_to_response('trackbox.html', {'videos': videos_with_metadata, 'page_type': page_type})

def trackinfo(request, lv_video_id):
	video = Video.objects.get(pk=lv_video_id)
	title = video.title
	channel_name = video.channel_name
	watch_page_url = video.watch_page_url

	now = timezone.now()

	upload_date_text = get_upload_date_text( video.upload_date, now )

	likes = Like.objects.filter(user=request.user.id, video_id=lv_video_id)
	class_name = ''
	alt_text = ''
	if likes:
		class_name = 'heart'
		alt_text = 'Remove this track from your playlist'
	else:
		class_name = 'plus'
		alt_text = 'Add this track to your playlist'
	return render_to_response('trackinfo.html', {'class_name': class_name, 'alt_text': alt_text, 'title': title, 'channel_name': channel_name, 'upload_date_text': upload_date_text, 'lv_video_id': lv_video_id, 'watch_page_url': watch_page_url})

def get_upload_date_text(upload_date, now):
	upload_date_text = ''
	
	year_delta = now.year - upload_date.year
	month_delta = now.month - upload_date.month
	day_delta = now.day - upload_date.day
	hour_delta = now.hour - upload_date.hour
	minute_delta = now.minute - upload_date.minute
	second_delta = now.second - upload_date.second

	if year_delta > 1:
		upload_date_text = 'Posted ' + str(year_delta) + ' years ago'
	elif year_delta == 1:
		upload_date_text = 'Posted ' + str(year_delta) + ' year ago'
	elif month_delta > 1:
		upload_date_text = 'Posted ' + str(month_delta) + ' months ago'
	elif month_delta == 1:
		upload_date_text = 'Posted ' + str(month_delta) + ' month ago'
	elif day_delta > 1:
		upload_date_text = 'Posted ' + str(day_delta) + ' days ago'
	elif day_delta == 1:
		upload_date_text = 'Posted ' + str(day_delta) + ' day ago'
	elif hour_delta > 1:
		upload_date_text = 'Posted ' + str(hour_delta) + ' hours ago'
	elif hour_delta == 1:
		upload_date_text = 'Posted ' + str(hour_delta) + ' hour ago'
	elif minute_delta > 1:
		upload_date_text = 'Posted ' + str(minute_delta) + ' minutes ago'
	elif minute_delta == 1:
		upload_date_text = 'Posted ' + str(minute_delta) + ' minute ago'
	elif second_delta > 1:
		upload_date_text = 'Posted ' + str(second_delta) + ' seconds ago'
	elif second_delta == 1:
		upload_date_text = 'Posted ' + str(second_delta) + ' second ago'
	else:
		upload_date_text = 'Posted now'

	return upload_date_text
	