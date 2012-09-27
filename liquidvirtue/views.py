from django.shortcuts import render_to_response, get_object_or_404
from liquidvirtue.models import User
from liquidvirtue.models import Like
from liquidvirtue.models import Channel
from liquidvirtue.models import Video
from datetime import datetime
from django.template import RequestContext

def index(request):
	if "np_video_id" in request.session:
		return render_to_response('index.html', {'np_video_id': request.session["np_video_id"]})
	else:
		return render_to_response('index.html', None, context_instance=RequestContext(request))
		
def index_with_id(request, np_video_id):
	return render_to_response('index.html', {'np_video_id': request.session["np_video_id"]})

def video_detail(request):
	page_type = request.GET["page_type"]
	video_id = request.GET["video_id"]
	v = '';
	if video_id == '':
		if page_type == 'my_library':
			id = request.user.id
			l = Like.objects.all().filter(lv_user_id=id)
			video = l.video_set().all().order_by('-upload_time')[0]
		elif page_type == 'popular':
			video = Video.objects.all().order_by('-upload_time').order_by('-num_likes')[0]
		else:
			#do newest
			video = Video.objects.all().order_by('-upload_time')[0]
	else:
		video = get_object_or_404(Video, vd=video_id)
	
	class_name = ''
	
	now = datetime.now()
	
	year_delta = now.year - video.upload_date.year;
	month_delta = now.month - video.upload_date.month;
	day_delta = now.day - video.upload_date.day;
	hour_delta = now.hour - video.upload_date.hour;
	minute_delta = now.minute - video.upload_date.minute;
	second_delta = now.second - video.upload_date.second;

	upload_date_text = ''
	if year_delta > 1:
		upload_date_text = 'Posted ' + year_delta + ' years ago'
	elif year_delta == 1:
		upload_date_text = 'Posted ' + year_delta + ' year ago'
	elif month_delta > 1:
		upload_date_text = 'Posted ' + month_delta + ' months ago'
	elif month_delta == 1:
		upload_date_text = 'Posted ' + month_delta + ' month ago'
	elif day_delta > 1:
		upload_date_text = 'Posted ' + day_delta + ' days ago'
	elif day_delta == 1:
		upload_date_text = 'Posted ' + day_delta + ' day ago'
	elif hour_delta > 1:
		upload_date_text = 'Posted ' + hour_delta + ' hours ago'
	elif hour_delta == 1:
		upload_date_text = 'Posted ' + hour_delta + ' hour ago'
	elif minute_delta > 1:
		upload_date_text = 'Posted ' + minute_delta + ' minutes ago'
	elif minute_delta == 1:
		upload_date_text = 'Posted ' + minute_delta + ' minute ago'
	elif second_delta > 1:
		upload_date_text = 'Posted ' + second_delta + ' seconds ago'
	elif second_delta == 1:
		upload_date_text = 'Posted ' + second_delta + ' second ago'
	else:
		upload_date_text = 'Posted now'

	return render_to_response('video_detail.html', {'video': video, 'page_type': page_type, 'upload_date_text': upload_date_text, 'class_name': class_name})

def trackbox_newest(request, page_number):
	page_number = int(page_number)
	videos = Video.objects.all().order_by('-upload_time')[(page_number-1)*17:(page_number*17)-1]
	
	now = datetime.now()
	
	upload_date_texts = []
	
	print now.year
	
	for video in videos:
		year_delta = now.year - video.upload_date.year;
		month_delta = now.month - video.upload_date.month;
		day_delta = now.day - video.upload_date.day;
		hour_delta = now.hour - video.upload_date.hour;
		minute_delta = now.minute - video.upload_date.minute;
		second_delta = now.second - video.upload_date.second;
	
		if year_delta > 1:
			upload_date_text = 'Posted ' + year_delta + ' years ago'
		elif year_delta == 1:
			upload_date_text = 'Posted ' + year_delta + ' year ago'
		elif month_delta > 1:
			upload_date_text = 'Posted ' + month_delta + ' months ago'
		elif month_delta == 1:
			upload_date_text = 'Posted ' + month_delta + ' month ago'
		elif day_delta > 1:
			upload_date_text = 'Posted ' + day_delta + ' days ago'
		elif day_delta == 1:
			upload_date_text = 'Posted ' + day_delta + ' day ago'
		elif hour_delta > 1:
			upload_date_text = 'Posted ' + hour_delta + ' hours ago'
		elif hour_delta == 1:
			upload_date_text = 'Posted ' + hour_delta + ' hour ago'
		elif minute_delta > 1:
			upload_date_text = 'Posted ' + minute_delta + ' minutes ago'
		elif minute_delta == 1:
			upload_date_text = 'Posted ' + minute_delta + ' minute ago'
		elif second_delta > 1:
			upload_date_text = 'Posted ' + second_delta + ' seconds ago'
		elif second_delta == 1:
			upload_date_text = 'Posted ' + second_delta + ' second ago'
		else:
			upload_date_text = 'Posted now'
		upload_date_texts.append(upload_date_text)
	
	return render_to_response('trackbox.html', {'videos': video, 'upload_date_texts': upload_date_texts})

def trackbox_popular(request, page_number):
	page_number = int(page_number)
	videos = Video.objects.all().order_by('-upload_time').order_by('-num_likes')[(page_number-1)*17:(page_number*17)-1]
	return render_to_response('trackbox.html', {'videos': videos})
	
def trackbox_my_library(request, page_number):
	page_number = int(page_number)
	id = request.user.id
	l = Like.objects.all().filter(user=id)
	videos = l.video_set().all().order_by('-upload_time')[(page_number-1)*17:(page_number*17)-1]
	return render_to_response('trackbox.html', {'videos': videos})