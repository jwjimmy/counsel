from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Hit(models.Model):
	hit_at = models.DateTimeField(auto_now_add=True)
	referer = models.CharField(max_length=1000)