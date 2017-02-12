from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.views.decorators.cache import cache_control

from counselapp.models import Hit
from counselapp.models import Visit
from counselapp.models import RequestMeta
from counselapp.models import RequestMetaForm
from counselapp.utils import get_visit_dict

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.edit import CreateView

import json
import logging
from PIL import Image

logger = logging.getLogger('django.request')

# Create your views here.

class RequestView(View):

	@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
	def get(self, request, *args, **kwargs):
		logger.info("Logging visit")

		visit = Visit.objects.create(**get_visit_dict(request.META))
		dump = json.dumps(json.loads(visit.metadata), sort_keys=True, indent=4, separators=(',',': '))
		logger.info("Successfully logged visit " + dump)

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

		logger.info("Before: " + str(type(form)))
		form = RequestMetaForm(initial)
		logger.info("After: " + str(type(form)))

		return super(RequestCreate, self).form_valid(form)

class HomeView(TemplateView):

    template_name = 'counselapp/home.html'
