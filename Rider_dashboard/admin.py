from django.contrib import admin
from Rider_dashboard.models.Rider import Rider


# Register your models here.

class RiderView(admin.ModelAdmin):
    list_display = ['name', 'CNIC', 'Rider_city', 'Callnumber', 'id', 'is_Active', 'assign_task']


admin.site.register(Rider, RiderView)
