from django.contrib import admin
from mainpage.models.Patient import Patient


# Register your models here.

class PatientView(admin.ModelAdmin):
    list_display = ['name', 'email', 'city', 'Address', 'id']


admin.site.register(Patient, PatientView)
