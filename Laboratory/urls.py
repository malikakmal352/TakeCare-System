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

from Laboratory.views import Labs, test_list, Booking_form, View_Your_Appointments, lab_search
from Laboratory.views import lab_admin, Lab_Login, add_new_test, test_delete, update_test, add_new_Samplest, \
    Status_samplest, Samplest_del, update_samplest, ChangePassword_Lab, ForgetPassword_Lab, Test_Booking_conformation, \
    Lab_profile, Lab_profile_img, upload_test_report, view_all_comfirm_booking, View_all_new_booking, view_test_list, \
    View_all_samplest, updates_lab_profile, Lab_logout

urlpatterns = [

    path('', lab_admin, name="lab_Admin"),
    path('Logout/', Lab_logout, name="Lab_logout"),

]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
