from django.db import models
from django_facebook.models import FacebookProfileModel
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(FacebookProfileModel):
    '''
    Inherit the properties from django facebook
    '''
    user = models.OneToOneField(User)

    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = UserProfile.objects.get_or_create(user=instance)

class Channel(models.Model):
	channel_name = models.CharField(max_length=500)
	newest_video_name = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.channel_name

class User(models.Model):
	facebook_username = models.CharField(max_length=500)
	facebook_id = models.IntegerField()

	def __unicode__(self):
		return self.facebook_username

class Video(models.Model):
	likes = models.ManyToManyField(User, through='Like')
	num_likes = models.IntegerField()
	channel = models.ForeignKey(Channel)
	channel_name = models.CharField(max_length=500)
	title = models.CharField(max_length=1000)
	youtube_video_id = models.CharField(max_length=1000)
	url = models.CharField(max_length=1000)
	watch_page_url = models.CharField(max_length=1000)
	upload_date = models.DateTimeField()
	featured = models.BooleanField()

	def __unicode__(self):
		return self.title

class Like(models.Model):
	user = models.ForeignKey(User)
	video = models.ForeignKey(Video)

	def __unicode__(self):
		return self.user