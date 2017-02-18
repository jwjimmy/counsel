from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.views.decorators.cache import cache_control

from counselapp.models import Hit, Visit, Estate
from counselapp.utils import get_visit_dict

from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views.generic.edit import CreateView

import json
import logging
from PIL import Image

logger = logging.getLogger('django.request')

# Create your views here.

class RequestView(View):

	@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
	def get(self, request, *args, **kwargs):
		uuid = self.kwargs.get("uuid", None)
		if uuid is None:
			raise SuspiciousOperation("Request requires a uuid")
		
		estate_count = Estate.objects.filter(uuid=uuid).count()
		if estate_count <= 0 or estate_count > 1:
			raise SuspiciousOperation("Invalid uuid")

		logger.info("Logging visit")

		visit = Visit.objects.create(**get_visit_dict(request.META, uuid))
		dump = json.dumps(json.loads(visit.metadata), sort_keys=True, indent=4, separators=(',',': '))
		logger.info("Successfully logged visit " + dump)

		red = Image.new('RGBA', (1, 1), (255,0,0,0))
		response = HttpResponse(content_type="image/jpeg")
		red.save(response, "JPEG")
		return response

class HitCreate(CreateView):

    model = Hit
    fields = []

class HomeView(TemplateView):

    template_name = 'counselapp/home.html'
