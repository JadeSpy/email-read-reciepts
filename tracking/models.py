from django.db import models
import datetime
import uuid
from django.utils import timezone


# Create your models here.
class Tracker(models.Model):
	id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
	recipient_email = models.EmailField()
	time_created = models.DateTimeField(default=timezone.now)
	recipient_name = models.CharField(max_length=100)
	email_subject = models.CharField(max_length=300)
	email_content = models.TextField()
	def __str__(self):
		return f"Tracker sent to {self.recipient_email} at {self.time_created}"
class TrackerHit(models.Model):
	tracker_id = models.ForeignKey(Tracker, on_delete=models.CASCADE)
	hit_date = models.DateTimeField(default=timezone.now)
	ip = models.CharField(max_length=100)


