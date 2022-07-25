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
from django.contrib import admin
from django.urls import path, include

import Rider_dashboard
from Rider_dashboard.urls import *

from Laboratory.views import Labs, test_list, Booking_form, View_Your_Appointments, lab_search
from Laboratory.views import lab_admin, Lab_Login, add_new_test, test_delete, update_test, add_new_Samplest, \
    Status_samplest, Samplest_del, update_samplest, ChangePassword_Lab, ForgetPassword_Lab, Test_Booking_conformation, \
    Lab_profile, Lab_profile_img, upload_test_report, view_all_comfirm_booking, View_all_new_booking, view_test_list, \
    View_all_samplest, updates_lab_profile

from TakeCare_System import settings

from mainpage.views import mainindex, Login, Signup, Logout, ForgetPassword, ChangePassword, Patient_Setting, \
    Change_patient_profile_img, updates_patient_profile, Save_Records, Add_new_Reports, view_report_detail, \
    Update_Reports, Save_Records_confirmation, About_us, Contact_us, Mobile_About_us

from Systemadmin.views import Super_admin, SuperAdmin_Login, ChangePassword_Admin, ForgetPassword_Admin, \
    view_Patient_list, Status_Patients, add_new_Patient, Patients_del, view_Labs_list, Status_Labs, add_new_Laboratory, \
    Laboratory_del, update_Laboratory, Admin_profile, Admin_profile_img, updates_admin_profile, view_N_D, \
    all_Register_doctor, Status_doctor, Add_new_Doctor, ADD_New_Pharmacy, view_Pharmacy_list, Status_Pharmacy, \
    Pharmacy_del, Update_Pharmacy, add_new_Rider, view_Rider_list, Status_Rider, view_New_Rider_Requests

from Doctor.views import Doctor_Login, ForgetPassword_doctor, ChangePassword_doctor, Doctor_request_form, \
    Create_password_doctor, view_all_doctors, Doctors_Special, Doctors_Special_in_city, Doctors_in_city, \
    view_specialities, Doctor_admin, Doctor_profile, updates_Doctor_profile, clinic_profile, updates_clinic_profile, \
    Health_blog, add_new_blog, view_Doctor_blogs, Update_health_blog, blog_detail, view_Full_Doctor_blogs, \
    blog_via_issue, New_Appointment_Requests, Confirm_appointments, Book_appointment, appointment_booked_Scheduled

from Pharmacy_Store.views import phy_login, Phy_admin, Create_password_Pharmacy, ForgetPassword_Pharmacy, \
    ChangePassword_Pharmacy, Phy_profile, updates_Phy_profile, Phy_profile_img, add_new_Medicine, view_Medicine_list, \
    Medicine_delete, update_Medicine, view_Expired_Medicine_list, view_Expiry_Soon_Medicine_list, Pharmacies, \
    Medicine_details, Tracking_Order, Cancel_order, Medicine_order_form, Order_Confirmed, order_cancel_confirm, \
    cart_add, cart_clear, item_decrement, item_increment, item_clear, cart_detail, Checkout, Order_Confirmed_by_Carts, \
    View_all_new_Orders, view_all_comfirm_Orders, view_all_complete_Orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path("about us/", About_us, name="About us"),
    path('Contact_us/', Contact_us, name="Contact_us"),
    path('Mobile_About_us/', Mobile_About_us, name="Mobile_About_us"),

    # ////////////////////////////////// URLS for Super Admin start//////////////////////////////////////////////
    path("Super_admin/", Super_admin, name="Super_admin"),
    path("SuperAdmin_Login/", SuperAdmin_Login, name="SuperAdmin_Login"),
    path("Admin_profile/", Admin_profile, name="Admin_profile"),
    path("Admin_profile_img/", Admin_profile_img, name="Admin_profile_img"),
    path("updates_admin_profile/", updates_admin_profile, name="updates_admin_profile"),

    path("view_Patient_list/", view_Patient_list, name="view_Patient_list"),
    path("Status_Patients/", Status_Patients, name="Status_Patients"),
    path("add_new_Patient/", add_new_Patient, name="add_new_Patient"),
    path("Patients_del/", Patients_del, name="Patients_del"),

    path("add_new_Laboratory/", add_new_Laboratory, name="add_new_Laboratory"),
    path("View_all_labs/", view_Labs_list, name="View_all_labs"),
    path("Status_Labs/", Status_Labs, name="Status_Labs"),
    path("Laboratory_del/", Laboratory_del, name="Laboratory_del"),
    path("update_Laboratory/<int:id>", update_Laboratory, name="update_Laboratory"),

    path("add_new_doctor/", Add_new_Doctor, name="add_new_doctor"),
    path("view_N_D/", view_N_D, name="view_N_D"),
    path("all_Register_doctor/", all_Register_doctor, name="all_Register_doctor"),
    path("Status_doctor/", Status_doctor, name="Status_doctor"),
    path("Create_password_doctor/<token>/", Create_password_doctor, name="Create_password_doctor"),

    path("ADD_New_Pharmacy/", ADD_New_Pharmacy, name="ADD_New_Pharmacy"),
    path("View ALL Pharmacy/", view_Pharmacy_list, name="view_Pharmacy_list"),
    path("Status_Pharmacy/", Status_Pharmacy, name="Status_Pharmacy"),
    path("Pharmacy_del/", Pharmacy_del, name="Pharmacy_del"),
    path("Update_Pharmacy/<int:id>/", Update_Pharmacy, name="Update_Pharmacy"),

    path('add_new_Rider/', add_new_Rider, name="add_new_Rider"),
    path('View_all_Rider/', view_Rider_list, name="view_Rider_list"),
    path('Status_Rider/', Status_Rider, name="Status_Rider"),
    path("Rider_Request/", view_New_Rider_Requests, name="Rider_Request"),

    # ////////////////////////////////// URLS for Super Admin END//////////////////////////////////////////////

    path('', mainindex, name='home'),

    # ////////////////////////////////// URLS for Laboratory Start//////////////////////////////////////////////

    path('lab_admin/', lab_admin, name="lab_Admin"),
    path('Lab_Login/', Lab_Login, name="Laboratory Login"),
    path("Lab_profile/", Lab_profile, name="Lab_profile"),
    path("Lab_profile_img/", Lab_profile_img, name="Lab_profile_img"),
    path("updates_lab_profile/", updates_lab_profile, name="updates_lab_profile"),
    path('Add_new_test/', add_new_test, name='add_new_test'),
    path("del/", test_delete, name='del_test'),
    path("update_test/", update_test, name='update_test'),

    path("add_new_Samplest/", add_new_Samplest, name='add_new_Samplest'),
    path("View_all_samplest/", View_all_samplest, name='View_all_samplest'),
    path("Status_samplest/", Status_samplest, name='Status_samplest'),
    path("Samplest_del/", Samplest_del, name='Samplest_del'),
    path("update_samplest/<int:id>", update_samplest, name='update_samplest'),

    path("Test_Booking_conformation/<int:id>", Test_Booking_conformation, name='Test_Booking_conformation'),
    path("upload_test_report/", upload_test_report, name="upload_test_report"),
    path("view_all_comfirm_booking/", view_all_comfirm_booking, name="view_all_comfirm_booking"),
    path("View_all_new_booking/", View_all_new_booking, name="View_all_new_booking"),
    path("view_test_list/", view_test_list, name="view_test_list"),

    # ////////////////////////////////// URLS for Laboratory END//////////////////////////////////////////////

    # ////////////////////////////////// URLS for Patient Start//////////////////////////////////////////////

    path('laboratory/<int:id>', Labs, name='Lab_page'),
    path('laboratory/', lab_search, name='Search via city'),

    path('View_list/<int:id>/', test_list, name='Laboratory test list'),
    path('Booking_form/<int:id>/', Booking_form, name='Lab test booking form'),
    path("Patient_Setting/", Patient_Setting, name="Patient_Setting"),
    path("patient_profile_img/", Change_patient_profile_img, name="Change_patient_profile_img"),
    path("updates_patient_profile/", updates_patient_profile, name="updates_patient_profile"),
    path('View_Your_Appointments/<int:id>/', View_Your_Appointments, name='View all Appointments,orders'),
    path("view_specialities/", view_specialities, name='view_specialities'),
    path('view_all_doctors/', view_all_doctors, name="view_all_doctors"),
    path("Doctors/<Speciality>/", Doctors_Special, name="Doctors_Special"),
    path("Doctors_by_city/<city>/", Doctors_in_city, name='Doctors_in_city'),
    path("Doctors/<Speciality>/<city>/", Doctors_Special_in_city, name='Doctors_Special_in_city'),
    path("Health_blog/", Health_blog, name="Health_blog"),
    path("Health_blog/<Health_blogs_issue>/<int:id>/", blog_detail, name="blog_detail"),
    path("Health_blog/<Health_blogs_issue>/", blog_via_issue, name="blog_via_issue"),
    path("Update_health_blog/", Update_health_blog, name="Update_health_blog"),
    path("Book_appointment/<int:id>/", Book_appointment, name="Book_appointment"),
    path("Book_appointment/<int:id>/Confirmation/", appointment_booked_Scheduled, name="Appointment_Confirmation"),

    path("Medical Records/", Save_Records, name="Save_medical_Records"),
    path("Medical Records/Add_new_Reports/", Add_new_Reports, name="Add_new_Reports"),
    path("view report detail/<int:id>/", view_report_detail, name="view report detail"),
    path("Medical Records/Update_Reports/<int:id>/", Update_Reports, name="Update_Reports"),
    path("Medical Records/<str:message>/", Save_Records_confirmation, name="Save_Records_confirmation"),

    path('Pharmacies/<int:id>', Pharmacies, name='Pharmacies_card_page'),
    path("Medicine_details/<int:id>", Medicine_details, name="Medicine_details"),
    path('Order Medicine Form/', Medicine_order_form, name="Medicine_order_form"),
    path('Order Confirmed/', Order_Confirmed, name="Order_Confirmed"),

    # path('Add to Carts/', carts, name='Add to Carts'),
    path('Carts/add/<int:id>/', cart_add, name='cart_add'),
    path('Carts/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('Carts/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('Carts/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('Carts/cart_clear/', cart_clear, name='cart_clear'),
    path('Carts/cart-detail/', cart_detail, name='cart_detail'),
    path('Carts_Checkout/', Checkout, name="Checkout_carts"),
    path('Order Confirmed by Carts/', Order_Confirmed_by_Carts, name="Order_Confirmed_by_Carts"),

    path("Tracking Order/", Tracking_Order, name="Tracking_Order"),
    path("Cancel Order/", Cancel_order, name="Cancel_order"),

    # ////////////////////////////////// URLS for Patient End//////////////////////////////////////////////

    # ////////////////////////////////// URLS for Doctor Start//////////////////////////////////////////////

    path("Doctor_admin/", Doctor_admin, name='Doctor_admin'),
    path("Doctor_profile/", Doctor_profile, name='Doctor_profile'),
    path("updates_Doctor_profile/", updates_Doctor_profile, name='updates_Doctor_profile'),
    path("clinic_profile/", clinic_profile, name="clinic_profile"),
    path("updates_clinic_profile/", updates_clinic_profile, name="updates_clinic_profile"),
    path("Doctor_admin/New_appointment_requests/", New_Appointment_Requests, name="New_Appointment_Requests"),
    path("Doctor_admin/confirm_today/", Confirm_appointments, name="Confirm_appointments"),

    path("add_new_blog/", add_new_blog, name="add_new_blog"),
    path("view_Doctor_blogs/", view_Doctor_blogs, name="view_Doctor_blogs"),
    path("view_Doctor_blogs/<int:id>/", view_Full_Doctor_blogs, name="view_Full_Doctor_blogs"),
    # ////////////////////////////////// URLS for Doctor Admin End//////////////////////////////////////////////

    # ////////////////////////////////// URLS for Pharmacy Admin Start//////////////////////////////////////////////
    path("Create_password_Pharmacy/<token>/", Create_password_Pharmacy, name="Create_password_Pharmacy"),
    path("Phy_Login/", phy_login, name="pharmacy Login"),
    path("Phy_admin/", Phy_admin, name="Phy_admin"),
    path("Phy_profile/", Phy_profile, name="Phy_profile"),
    path("Phy_profile_img/", Phy_profile_img, name="Phy_profile_img"),
    path("updates_Phy_profile/", updates_Phy_profile, name="updates_Phy_profile"),

    path("add_new_Medicine/", add_new_Medicine, name="add_new_Medicine"),
    path("View_all_Medicine/", view_Medicine_list, name="view_Medicine_list"),
    path("Medicine delete/", Medicine_delete, name="Medicine_delete"),
    path("Update Medicine/", update_Medicine, name="update_Medicine"),
    path("View_all_Expiry Medicine/", view_Expired_Medicine_list, name="view_Expired_Medicine_list"),
    path("View Expiring Soon/", view_Expiry_Soon_Medicine_list, name="view_Expiry_Soon_Medicine_list"),

    path("Phy_admin/View_all_new_Orders/", View_all_new_Orders, name="View_all_new_Orders"),
    path("Phy_admin/view_all_comfirm_Orders/", view_all_comfirm_Orders, name="view_all_comfirm_Orders"),
    path('Phy_admin/view complete orders/', view_all_complete_Orders, name="view_all_complete_Orders"),

    path('order_cancel_confirm/', order_cancel_confirm, name='order_cancel_confirm'),

    # ////////////////////////////////// URLS for Pharmacy Admin End//////////////////////////////////////////////

    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////

    path("Rider_Login/", Rider_Login, name="Rider_Login"),
    path("Rider_Dashboard/", include(Rider_dashboard.urls)),
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////

    path('register/', Signup),
    path('Login/', Login, name='login'),
    path('Logout/', Logout, name='Logout'),

    path("Doctor_Login/", Doctor_Login, name="Doctor_Login"),
    path("Doctor_request_form/", Doctor_request_form, name="Doctor_request_form"),

    path('forget-password/', ForgetPassword, name="forget_password"),
    path('change-password/<token>/', ChangePassword, name="change_password"),

    path('forget-password_Lab/', ForgetPassword_Lab, name="forget_password_Lab"),
    path('change-password_Lab/<token>/', ChangePassword_Lab, name="change_password_Lab"),

    path('forget-password_doctor/', ForgetPassword_doctor, name="ForgetPassword_doctor"),
    path('change-password_doctor/<token>/', ChangePassword_doctor, name="change_password_doctor"),

    path('forget-password Pharmacy/', ForgetPassword_Pharmacy, name="ForgetPassword_Pharmacy"),
    path('change-password_Pharmacy/<token>/', ChangePassword_Pharmacy, name="ChangePassword_Pharmacy"),

    path('ForgetPassword_Admin/', ForgetPassword_Admin, name="ForgetPassword_Admin"),
    path('ChangePassword_Admin/<token>/', ChangePassword_Admin, name="ChangePassword_Admin"),

]

handler404 = 'mainpage.views.not_found'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
