from django.contrib import admin
from counselapp.models import Hit
from counselapp.models import Visit
from counselapp.models import RequestMeta

class HitAdmin(admin.ModelAdmin):
	list_display = ('hit_at', 'referer')

class RequestMetaAdmin(admin.ModelAdmin):
	list_display = [item.name for item in RequestMeta._meta.fields]

class VisitAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'metadata')

# Register your models here.


admin.site.register(Hit, HitAdmin)
admin.site.register(RequestMeta, RequestMetaAdmin)
admin.site.register(Visit, VisitAdmin)