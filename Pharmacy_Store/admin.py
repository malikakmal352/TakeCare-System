from django.contrib import admin
from Pharmacy_Store.models.Add_pharmacy import Pharmacy
from Pharmacy_Store.models.Add_Medicine import Add_New_Medicine


# Register your models here.

class PharmacyView(admin.ModelAdmin):
    list_display = ["Pharmacy_name", "email", "city", 'id', "is_Active"]


class New_MedicineView(admin.ModelAdmin):
    list_display = ["Medicine_name", "Medicine_price", "Medicine_Expiry_date", "Total_Stock", "Pharmacy", "id", "is_Expired"]


admin.site.register(Pharmacy, PharmacyView)
admin.site.register(Add_New_Medicine, New_MedicineView)
