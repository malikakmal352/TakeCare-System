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

from mainpage.views import mainindex, Login, Signup, Logout, ForgetPassword, ChangePassword, Patient_Setting, \
    Change_patient_profile_img, updates_patient_profile, Save_Records, Add_new_Reports, view_report_detail, \
    Update_Reports, Save_Records_confirmation, About_us, Contact_us, Mobile_About_us, Customer_Logout

urlpatterns = [

    path('', mainindex, name='home'),

    path('register/', Signup),
    path('Login/', Login, name='login'),
    path('Logout/', Logout, name='Logout'),
    path('Customer_Logout/', Customer_Logout, name='Customer_Logout'),

    path("Patient_Setting/", Patient_Setting, name="Patient_Setting"),
    path("patient_profile_img/", Change_patient_profile_img, name="Change_patient_profile_img"),
    path("updates_patient_profile/", updates_patient_profile, name="updates_patient_profile"),

    path("Medical Records/", Save_Records, name="Save_medical_Records"),
    path("Medical Records/Add_new_Reports/", Add_new_Reports, name="Add_new_Reports"),
    path("view report detail/<int:id>/", view_report_detail, name="view report detail"),
    path("Medical Records/Update_Reports/<int:id>/", Update_Reports, name="Update_Reports"),
    path("Medical Records/<str:message>/", Save_Records_confirmation, name="Save_Records_confirmation"),

    path('forget-password/', ForgetPassword, name="forget_password"),
    path('change-password/<token>/', ChangePassword, name="change_password"),

]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
