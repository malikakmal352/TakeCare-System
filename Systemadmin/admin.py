from django.contrib import admin
from Systemadmin.models.Super_Admin import SuperAdmin
# Register your models here.

class SuperAdminView(admin.ModelAdmin):
    list_display = ['Username', 'email', 'Callnumber', 'is_Active']


admin.site.register(SuperAdmin)