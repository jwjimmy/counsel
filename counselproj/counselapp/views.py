from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from counselapp.models import Hit
from counselapp.models import RequestMeta
from counselapp.models import RequestMetaForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.edit import CreateView

import json
import copy
from PIL import Image

# Create your views here.

class RequestView(View):

	def get(self, request, *args, **kwargs):
		fields = [x.name.upper() for x in RequestMeta._meta.fields]
		keys = [key for key in self.request.META.keys() if key in fields]
		initial = { key.lower() : self.request.META[key] for key in keys }

		form = RequestMeta(**initial)
		print "After: " + str(form)
		print initial

		form.save()

		red = Image.new('RGBA', (1, 1), (255,0,0,0))
		response = HttpResponse(content_type="image/jpeg")
		red.save(response, "JPEG")
		return response

class HitCreate(CreateView):

    model = Hit
    fields = []

class RequestCreate(CreateView):

	model = RequestMeta
	fields = []

	def form_valid(self, form):
		fields = [x.name.upper() for x in RequestMeta._meta.fields]
		keys = [key for key in self.request.META.keys() if key in fields]
		initial = { key.lower() : self.request.META[key] for key in keys }

		print "Before: " + str(type(form))
		form = RequestMetaForm(initial)
		print "After: " + str(type(form))

		return super(RequestCreate, self).form_valid(form)

class HomeView(TemplateView):

    template_name = 'counselapp/home.html'
