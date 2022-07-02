from django.contrib import admin
from Pharmacy_Store.models.Add_pharmacy import Pharmacy
from Pharmacy_Store.models.Add_Medicine import Add_New_Medicine
from Pharmacy_Store.models.Medicine_Order import order


# Register your models here.

class PharmacyView(admin.ModelAdmin):
    list_display = ["Pharmacy_name", "email", "city", 'id', "is_Active"]


class New_MedicineView(admin.ModelAdmin):
    list_display = ["Medicine_name", "Medicine_price", "Medicine_Expiry_date", "Total_Stock", "Pharmacy", "id",
                    "is_Expired"]


class Medicine_Order_View(admin.ModelAdmin):
    list_display = ["Customer", "Medicine", "quantity", "Total_price", "order_date", "Delivery_by","status", "id"]


admin.site.register(Pharmacy, PharmacyView)
admin.site.register(Add_New_Medicine, New_MedicineView)
admin.site.register(order, Medicine_Order_View)
