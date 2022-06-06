from django.db import models
from Laboratory.models.Labcity import Labcity
# Create your models here.

class Lab(models.Model):
    homesampling = (
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    )

    Labname = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='lablogo/', default='', null=True, blank=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    Callnumber = models.PositiveIntegerField(default=1)
    city = models.ForeignKey(Labcity, on_delete=models.CASCADE, default=1)
    Address = models.TextField(max_length=300, default="")
    Home_Sample = models.CharField(max_length=200, null=True, choices=homesampling, default='Available')
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.Labname

    def get_by_email(email):
        try:
            return Lab.objects.get(email=email)
        except:
            return False

    def isExits(self):
        if Lab.objects.filter(email=self.email):
            return True

        return False
