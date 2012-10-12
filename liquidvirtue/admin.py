from django.contrib import admin
from liquidvirtue.models import Video, Channel

admin.site.register(Video, Channel)