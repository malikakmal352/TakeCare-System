from django.db import models
from Laboratory.models.Labcity import Labcity
from Laboratory.models.add_lab import Lab
# Create your models here.

class Rider(models.Model):
    # homesampling = (
    #     ('Available', 'Available'),
    #     ('Not Available', 'Not Available'),
    # )

    name = models.CharField(max_length=200, default='')
    CNIC = models.BigIntegerField(default=0)
    Rider_city = models.CharField(max_length=100)
    Callnumber = models.BigIntegerField(default=1)
    img = models.ImageField(upload_to='Rider_img/', default='')
    password = models.CharField(max_length=100, default='')
    # Laboratory = models.ForeignKey(Lab, on_delete=models.CASCADE, default=1)
    forget_password_token = models.CharField(max_length=100, null=True)
    is_Active = models.BooleanField(default=True)
    assign_task = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    # def get_by_CNIC(CNIC):
    #     try:
    #         return Samplest.objects.get(CNIC=CNIC)
    #     except:
    #         return False

    def CNIC_isExits(self):
        if Rider.objects.filter(CNIC=self.CNIC):
            return True

        return False
