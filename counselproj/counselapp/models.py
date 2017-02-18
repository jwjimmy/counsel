from __future__ import unicode_literals

from django.db import models
from django import forms

# Create your models here.

class Hit(models.Model):
	hit_at = models.DateTimeField(auto_now_add=True)
	referer = models.CharField(max_length=1000)

class Visit(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	url = models.CharField(max_length=1000, default="")
	visitor = models.CharField(max_length=2000, default="")
	metadata = models.TextField()
