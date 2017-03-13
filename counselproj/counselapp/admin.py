from django.contrib import admin
from counselapp.models import Hit
from counselapp.models import Visit
from counselapp.models import Estate

class HitAdmin(admin.ModelAdmin):
	list_display = ('hit_at', 'referer')

class VisitAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'estate', 'visitor', 'metadata')

class VisitInline(admin.TabularInline):
	model = Visit

class EstateAdmin(admin.ModelAdmin):
	list_display = ('created_at', 'uuid', 'description', 'estate_type')
	inlines = [
		VisitInline,
	]

# Register your models here.


admin.site.register(Hit, HitAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Estate, EstateAdmin)