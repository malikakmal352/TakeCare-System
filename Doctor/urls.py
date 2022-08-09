"""TakeCare_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path
from TakeCare_System import settings
from Doctor.views import Doctor_Login, ForgetPassword_doctor, ChangePassword_doctor, Doctor_request_form, \
    Create_password_doctor, view_all_doctors, Doctors_Special, Doctors_Special_in_city, Doctors_in_city, \
    view_specialities, Doctor_admin, Doctor_profile, updates_Doctor_profile, clinic_profile, updates_clinic_profile, \
    Health_blog, add_new_blog, view_Doctor_blogs, Update_health_blog, blog_detail, view_Full_Doctor_blogs, \
    blog_via_issue, New_Appointment_Requests, Confirm_appointments, Book_appointment, appointment_booked_Scheduled,\
    Give_Review

urlpatterns = [

    path("", Doctor_admin, name='Doctor_admin'),

]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
