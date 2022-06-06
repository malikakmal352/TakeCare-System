from django.db import models
# from Laboratory.models.Labcity import Labcity
# Create your models here.

class SuperAdmin(models.Model):

    Username = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='lablogo/', null=True, blank=True )
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    Callnumber = models.BigIntegerField(blank=True, null=True)
    Whatsapp = models.BigIntegerField(blank=True, null=True)
    Address = models.TextField(max_length=300, default="")
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def get_by_email(email):
        try:
            return SuperAdmin.objects.get(email=email)
        except:
            return False

    def isExits(self):
        if SuperAdmin.objects.filter(email=self.email):
            return True

        return False
