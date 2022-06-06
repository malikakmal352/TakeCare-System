from django.db import models
from Laboratory.models.Labcity import Labcity
from Laboratory.models.add_lab import Lab
# Create your models here.

class Test_list(models.Model):
    Test_name = models.CharField(max_length=200, default='')
    test_price = models.DecimalField(default=0, blank=True, max_digits=5,  decimal_places=1)
    laboratory = models.ForeignKey(Lab, on_delete=models.CASCADE, default='')
    # Address = models.TextField(max_length=500, blank=True, null=True, default='')
    Home_Sample = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.Test_name