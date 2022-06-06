from django.contrib import admin
from Laboratory.models.add_lab import Lab
from Laboratory.models.Labcity import Labcity
from Laboratory.models.Lab_tests_list import Test_list
from Laboratory.models.Book_lab_test import Book_Test
from Laboratory.models.Samplest import Samplest


# Register your models here.

class LabView(admin.ModelAdmin):
    list_display = ['Labname', 'email', 'city', 'Address']


class BookTestView(admin.ModelAdmin):
    list_display = ['Patient_Name', 'Book_Test', 'Test_Type', 'status', 'Laboratory', 'Address']


class SamplestView(admin.ModelAdmin):
    list_display = ['name', 'CNIC', 'Laboratory', 'is_Active']


admin.site.register(Lab, LabView)
admin.site.register(Labcity)
admin.site.register(Test_list)
admin.site.register(Book_Test, BookTestView)
admin.site.register(Samplest, SamplestView)
