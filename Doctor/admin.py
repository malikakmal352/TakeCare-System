from django.contrib import admin
from Doctor.models.Doctor_Request import Doctor_request
from Doctor.models.ADD_Docror import Doctors
from Doctor.models.All_Specialist import Special
from Doctor.models.Clinic import Clinic
from Doctor.models.Health_blog import Health_blogs
from Doctor.models.appointments import Appointment
from Doctor.models.save_reports import Save_Medical_Reports


# Register your models here.

class DoctorView(admin.ModelAdmin):
    list_display = ['Doctor_name', 'email', 'city', 'Speciality', 'Doctor_PMID_number', 'is_Active', 'is_Live']


class Doctor_requestView(admin.ModelAdmin):
    list_display = ['Doctor_name', 'email', 'city', 'Speciality', 'Doctor_PMID_number', 'Gender', 'Status',
                    'is_Accepted']


class Doctor_SpecialityView(admin.ModelAdmin):
    list_display = ['id', 'Doctor_Speciality', 'img', 'total_doctors']


class Health_blogsView(admin.ModelAdmin):
    list_display = ['Health_blogs_issue', 'Main_heading', 'Doctor', 'blog_create_time', 'id']


class Save_reportsView(admin.ModelAdmin):
    list_display = ['Report_Title', 'Doctor_name', 'Patient_name', 'Patient', 'id']


admin.site.register(Doctors, DoctorView)
admin.site.register(Doctor_request, Doctor_requestView)
admin.site.register(Special, Doctor_SpecialityView)
admin.site.register(Health_blogs, Health_blogsView)
admin.site.register(Clinic)
admin.site.register(Appointment)
admin.site.register(Save_Medical_Reports, Save_reportsView)