"""counselproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt
from counselapp.views import HomeView
from counselapp.views import HitCreate
from counselapp.views import RequestView, EstateView, EstateList
from rest_framework import routers, serializers, viewsets
from fcm.views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)

urlpatterns = [
    url(r'^login/', auth_views.login, {'template_name': 'counselapp/login.html'}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', auth_views.logout, name='logout'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^fcm/', include('fcm.urls')),
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^hits/create$', csrf_exempt(HitCreate.as_view(success_url="/hits/create"))),
    url(r'^requests/passive/(?P<uuid>.+)$', csrf_exempt(RequestView.as_view())),
    url(r'^estate/(?P<uuid>.+)$', EstateView.as_view(), name='estate'),
    url(r'^user/(?P<user_id>[a-zA-Z0-9_]+)$', EstateList.as_view(), name='estate-list'),
]
