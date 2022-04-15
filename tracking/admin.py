from django.contrib import admin

from .models import Tracker,TrackerHit

admin.site.register(Tracker)
admin.site.register(TrackerHit)