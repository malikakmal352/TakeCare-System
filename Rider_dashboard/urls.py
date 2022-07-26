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

from Rider_dashboard.views import Rider_Login, Rider_Dashboard, Rider_delivery, View_Complete_Deliveries, \
    View_Pending_Deliveries, Deliveries_History, Rider_profile, Rider_profile_img, updates_Rider_profile, \
    Rider_Logout

urlpatterns = [
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////

    path("", Rider_Dashboard, name="Rider_Dashboard"),
    path("Rider_delivery/", Rider_delivery, name="Rider_delivery"),
    path("view complete orders/", View_Complete_Deliveries, name="View_Complete_Deliveries"),
    path("view_all_pending_Orders/", View_Pending_Deliveries, name="View_Pending_Deliveries"),
    path("Delivery orders History/", Deliveries_History, name="Deliveries_History"),

    path("Rider_Profile/", Rider_profile, name="Rider_profile"),
    path('Rider_profile_img/', Rider_profile_img, name="Rider_profile_img"),
    path("updates_Rider_profile/", updates_Rider_profile, name="updates_Rider_profile"),

    path('Rider_Logout/', Rider_Logout, name='Rider_Logout'),
    # ////////////////////////////////// URLS for Rider Admin End//////////////////////////////////////////////


]

handler404 = 'mainpage.views.not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
