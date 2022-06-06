from django.db import models
from Laboratory.models.Labcity import Labcity

# Create your models here.
class Pharmacy(models.Model):
    homesampling = (
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    )

    Pharmacy_name = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='Phy_logo/', default='', null=True, blank=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    Callnumber = models.PositiveBigIntegerField(default=1)
    city = models.ForeignKey(Labcity, on_delete=models.CASCADE, default=1)
    Address = models.TextField(max_length=300, default="")
    Note = models.TextField(default="", max_length=300)
    # Home_Sample = models.CharField(max_length=200, null=True, choices=homesampling, default='Available')
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.Pharmacy_name

    def get_by_email(email):
        try:
            return Pharmacy.objects.get(email=email)
        except:
            return False

    def isExits(self):
        if Pharmacy.objects.filter(email=self.email):
            return True

        return False
