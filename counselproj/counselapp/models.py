from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib.auth.models import User

from fcm.models import AbstractDevice

import uuid

# Create your models here.

class CounselDevice(AbstractDevice):
	user = models.ForeignKey(User)
	class Meta(AbstractDevice.Meta):
		swappable = 'FCM_DEVICE_MODEL'

class Hit(models.Model):
	hit_at = models.DateTimeField(auto_now_add=True)
	referer = models.CharField(max_length=1000)

class Estate(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=500, default="")
	description = models.CharField(max_length=1000, default="")
	estate_type = models.IntegerField()
	owner = models.ForeignKey(User, related_name="estates")

	def __unicode__(self):
		return self.name

class Visit(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	url = models.CharField(max_length=1000, default="")
	visitor = models.CharField(max_length=2000, default="")
	metadata = models.TextField()
	estate = models.ForeignKey(Estate, related_name="visits")

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField()
