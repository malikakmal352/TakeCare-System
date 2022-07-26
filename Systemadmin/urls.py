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

from Systemadmin.views import Super_admin, SuperAdmin_Login, ChangePassword_Admin, ForgetPassword_Admin, \
    view_Patient_list, Status_Patients, add_new_Patient, Patients_del, view_Labs_list, Status_Labs, add_new_Laboratory, \
    Laboratory_del, update_Laboratory, Admin_profile, Admin_profile_img, updates_admin_profile, view_N_D, \
    all_Register_doctor, Status_doctor, Add_new_Doctor, ADD_New_Pharmacy, view_Pharmacy_list, Status_Pharmacy, \
    Pharmacy_del, Update_Pharmacy, add_new_Rider, view_Rider_list, Status_Rider, view_New_Rider_Requests, \
    Super_admin_logout

urlpatterns = [
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////
    #
    path("", Super_admin, name="Super_admin"),
    # path("Rider_delivery/", Rider_delivery, name="Rider_delivery"),
    # path("view complete orders/", View_Complete_Deliveries, name="View_Complete_Deliveries"),
    # path("view_all_pending_Orders/", View_Pending_Deliveries, name="View_Pending_Deliveries"),
    # path("Delivery orders History/", Deliveries_History, name="Deliveries_History"),
    #
    # path("Rider_Profile/", Rider_profile, name="Rider_profile"),
    # path('Rider_profile_img/', Rider_profile_img, name="Rider_profile_img"),
    # path("updates_Rider_profile/", updates_Rider_profile, name="updates_Rider_profile"),
    #
    path('Super_admin_logout/', Super_admin_logout, name='Super_admin_logout'),
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////


]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
