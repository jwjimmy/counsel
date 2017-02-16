from django.contrib import admin
from counselapp.models import Hit
from counselapp.models import Visit

class HitAdmin(admin.ModelAdmin):
	list_display = ('hit_at', 'referer')

class VisitAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'estate', 'visitor', 'metadata')

# Register your models here.


admin.site.register(Hit, HitAdmin)
admin.site.register(Visit, VisitAdmin)