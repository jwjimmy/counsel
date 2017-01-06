from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import View
from counselapp.models import Hit
from django.http import JsonResponse
from django.views.generic.edit import CreateView

# Create your views here.

class HitCreate(CreateView):

    model = Hit
    fields = ['referer']

    def form_valid(self, form):
    	print self.request.META

    def get_referer(request):
	    referer = request.META.get('HTTP_REFERER')
	    return referer

class HomeView(TemplateView):

    template_name = 'counselapp/home.html'
