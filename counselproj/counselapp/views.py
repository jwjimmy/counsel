from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.decorators.cache import cache_control

from counselapp.models import Hit, Visit, Estate, UserProfile
from counselapp.utils import get_visit_dict, send_to_android
from counselapp.forms import RegistrationForm

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.core.exceptions import SuspiciousOperation
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.gis.geoip2 import GeoIP2#, GeoIP2Exception
from geoip2.errors import AddressNotFoundError
import datetime, random, sha

import json
import logging
from PIL import Image

logger = logging.getLogger('django.request')

# Create your views here.

class UserLoggedOut(View):

	template_name = "counselapp/logout.html"

	def get(self, request):
		response = logout(request)

		return render(response, self.template_name)

class UserSignUpSuccess(TemplateView):

	template_name = "counselapp/signup_success.html"

class UserSignUp(TemplateView):
	
	template_name = "counselapp/signup.html"

	def get(self, request):
		if self.request.user.is_authenticated():
			return render(request, 'counselapp/signup.html', {'has_account': True})
		else:
			return super(UserSignUp, self).get(request)

	def get_context_data(self):
		context = {}
		context['form'] = RegistrationForm()
		return context

	def post(self, request):

		form = RegistrationForm(self.request.POST)

		if self.request.user.is_authenticated():
			return render(request, 'counselapp/signup.html', {'has_account': True})

		if form.is_valid():
			#import pdb; pdb.set_trace()
			new_user = form.save(form.cleaned_data)

			# Build the activation key for their account                                                                                                                    
			salt = sha.new(str(random.random())).hexdigest()[:5]
			activation_key = sha.new(salt+new_user.username).hexdigest()
			key_expires = now() + datetime.timedelta(2)

			# Create and save their profile                                                                                                                                 
			new_profile = UserProfile(user=new_user,
									  activation_key=activation_key,
									  key_expires=key_expires)
			new_profile.save()
			
			# Send an email with the confirmation link                                                                                                                      
			email_subject = 'Your new example.com account confirmation'
			email_body = "Hi %s, thanks for signing up. <br> \
			To activate your account, click this link within 48 hours:<br> \
			http://localhost:8000/accounts/confirm/%s" % (
				new_user.username,
				new_profile.activation_key)
			send_mail(email_subject,
						email_body,
						'accounts@example.com',
						[new_user.email],
						fail_silently=False)
			logger.info("Successful form submission")
			return HttpResponseRedirect(reverse('signup-success'))
		else:
			logger.info("Invalid form")
			return render(request, 'counselapp/signup.html', {'form': form})

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

	def get_context_data(self):
		context = {}
		if self.request.user.is_authenticated():
			context['has_account'] = True
		return context