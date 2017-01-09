from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from counselapp.models import Hit
from counselapp.models import RequestMeta
from counselapp.models import RequestMetaForm
from django.http import JsonResponse
from django.views.generic.edit import CreateView

import json
import copy

# Create your views here.

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
