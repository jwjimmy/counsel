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
from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from counselapp.views import HomeView
from counselapp.views import HitCreate
from counselapp.views import RequestCreate
from counselapp.views import RequestView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view()),
    url(r'^hits/create$', csrf_exempt(HitCreate.as_view(success_url="/hits/create"))),
    url(r'^requests/create$', csrf_exempt(RequestCreate.as_view(success_url="/requests/create"))),
    url(r'^requests/passive$', csrf_exempt(RequestView.as_view())),
]
