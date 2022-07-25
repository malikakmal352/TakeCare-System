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

from Pharmacy_Store.views import *
from mainpage.views import mainindex, Login, Signup, Logout, ForgetPassword, ChangePassword, Patient_Setting, \
    Change_patient_profile_img, updates_patient_profile, Save_Records, Add_new_Reports, view_report_detail, \
    Update_Reports, Save_Records_confirmation, About_us, Contact_us, Mobile_About_us

urlpatterns = [
    path('forget-password/', ForgetPassword, name="forget_password"),
    path('change-password/<token>/', ChangePassword, name="change_password"),


    path('forget-password Pharmacy/', ForgetPassword_Pharmacy, name="ForgetPassword_Pharmacy"),
    path('change-password_Pharmacy/<token>/', ChangePassword_Pharmacy, name="ChangePassword_Pharmacy"),


]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
