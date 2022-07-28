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

from Pharmacy_Store.views import phy_login, Phy_admin, Create_password_Pharmacy, ForgetPassword_Pharmacy, \
    ChangePassword_Pharmacy, Phy_profile, updates_Phy_profile, Phy_profile_img, add_new_Medicine, view_Medicine_list, \
    Medicine_delete, update_Medicine, view_Expired_Medicine_list, view_Expiry_Soon_Medicine_list, Pharmacies, \
    Medicine_details, Tracking_Order, Cancel_order, Medicine_order_form, Order_Confirmed, order_cancel_confirm, \
    cart_add, cart_clear, item_decrement, item_increment, item_clear, cart_detail, Checkout, Order_Confirmed_by_Carts, \
    View_all_new_Orders, view_all_comfirm_Orders, view_all_complete_Orders, All_Medicines, Phy_logout

urlpatterns = [
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////

    path("", Phy_admin, name="Phy_admin"),

    path('Logout/', Phy_logout, name='Phy_logout'),
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////


]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
