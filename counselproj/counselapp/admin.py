from django.contrib import admin
from counselapp.models import Hit

class HitAdmin(admin.ModelAdmin):
	list_display = ('hit_at', 'referer')

# Register your models here.


admin.site.register(Hit, HitAdmin)