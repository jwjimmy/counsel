from __future__ import unicode_literals

from django.db import models
from django import forms

# Create your models here.

class Hit(models.Model):
	hit_at = models.DateTimeField(auto_now_add=True)
	referer = models.CharField(max_length=1000)

class Visit(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	estate = models.CharField(max_length=1000, blank=True)
	visitor = models.CharField(max_length=2000, blank=True)
	metadata = models.TextField()

class RequestMeta(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	http_referer = models.CharField(max_length=1000)
	server_software = models.CharField(max_length=1000)
	http_origin = models.CharField(max_length=1000)
	server_protocol = models.CharField(max_length=1000)
	systemroot = models.CharField(max_length=1000)
	http_referer = models.CharField(max_length=1000)
	virtual_env = models.CharField(max_length=1000)
	java_home = models.CharField(max_length=1000)
	http_referer = models.CharField(max_length=1000)
	path = models.CharField(max_length=5000)
	http_cookie = models.CharField(max_length=1000)
	computername = models.CharField(max_length=1000)
	userdomain = models.CharField(max_length=1000)
	http_referer = models.CharField(max_length=1000)
	remote_addr = models.CharField(max_length=1000)

class RequestMetaForm(forms.ModelForm):
	class Meta:
		model = RequestMeta
		fields = [item.name for item in RequestMeta._meta.fields if item.name != "created_at"]