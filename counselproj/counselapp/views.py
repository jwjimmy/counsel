from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.decorators.cache import cache_control

from counselapp.models import Hit, Visit, Estate
from counselapp.utils import get_visit_dict, send_to_android

from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.gis.geoip2 import GeoIP2#, GeoIP2Exception
from geoip2.errors import AddressNotFoundError

import json
import logging
from PIL import Image

logger = logging.getLogger('django.request')

# Create your views here.

@method_decorator(login_required, name='dispatch')
class UserHome(ListView):
	model = Estate

	def get_queryset(self):
		user_id = self.request.user.id
		return Estate.objects.filter(owner=user_id)

	def get_context_data(self):
		user_id = self.request.user.id
		user = User.objects.get(id=user_id)

		context = {}
		context['username'] = user.username
		context['object_list'] = self.get_queryset()
		return context

@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class EstateList(ListView):
	model = Estate

	def get_queryset(self):
		user_id = self.kwargs['user_id']
		return Estate.objects.filter(owner=user_id)

	def get_context_data(self):
		user_id = self.kwargs['user_id']
		user = User.objects.get(id=user_id)

		context = {}
		context['username'] = user.username
		context['object_list'] = self.get_queryset()
		return context

@method_decorator(login_required, name='dispatch')
class EstateView(ListView):
	model = Visit

	def get_queryset(self):
		uuid = self.kwargs['uuid']
		print uuid
		return Visit.objects.filter(estate=uuid).order_by('created_at').reverse()

	def get_context_data(self):
		g = GeoIP2()
		visits = self.get_queryset()
		for visit in visits:
			try:
				visit.location = g.city(visit.visitor)['city']
			except AddressNotFoundError as e:
				pass

		context = {}
		context['estate'] = Estate.objects.get(uuid=self.kwargs['uuid'])
		context['object_list'] = visits
		return context

class RequestView(View):

	def generate_pixel(self):
		red = Image.new('RGBA', (1, 1), (255,0,0,0))
		response = HttpResponse(content_type="image/jpeg")
		red.save(response, "JPEG")
		return response

	@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
	def get(self, request, *args, **kwargs):
		uuid = self.kwargs.get("uuid", None)
		if uuid is None:
			raise SuspiciousOperation("Request requires a uuid")
		
		estate_count = Estate.objects.filter(uuid=uuid).count()
		if estate_count <= 0 or estate_count > 1:
			raise SuspiciousOperation("Invalid uuid")

		estate = Estate.objects.get(uuid=uuid)
		if str(estate) == "the-creatives/ml-drinks":
			send_to_android(str(estate))

		if "HTTP_REFERER" in request.META.keys() and "localhost" in request.META["HTTP_REFERER"]:
			logger.info("Discard localhost referer")
			return self.generate_pixel()

		logger.info("Logging visit for estate " + str(estate))
		visit = Visit.objects.create(**get_visit_dict(request.META, uuid))
		dump = json.dumps(json.loads(visit.metadata), sort_keys=True, indent=4, separators=(',',': '))
		logger.info("Successfully logged visit " + dump)

		return self.generate_pixel()

class HitCreate(CreateView):

    model = Hit
    fields = []

class HomeView(TemplateView):

    template_name = 'counselapp/home.html'
