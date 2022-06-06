import datetime

from django.utils import timezone

from django.db import models
from Pharmacy_Store.models.Add_pharmacy import Pharmacy


class Add_New_Medicine(models.Model):
    Medicine_Packaging = (
        ('Blister packs', 'Blister packs'),
        ('Bottles\Sachets', 'Bottles\Sachets'),
    )
    Status = (
        ("Active", "Active"),
        ("Delete", "Delete"),
        ("Out of Stock", "Out of Stock"),
    )
    img = models.ImageField(null=True, blank=True, upload_to='Medicine_img')
    Medicine_name = models.CharField(max_length=255)
    Medicine_price = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    Medicine_Expiry_date = models.DateField()
    Expiry_Alert_Date = models.DateField(default=timezone.now)
    Total_Stock = models.PositiveIntegerField(default=0)
    Pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default='')
    Medicine_packaging = models.CharField(max_length=200, null=True, choices=Medicine_Packaging,
                                          default='Blister packs')
    Description = models.TextField(default='', blank=True, null=True)
    status = models.CharField(max_length=200, choices=Status, default='Active')
    is_Expired = models.BooleanField(default=False)

    def __str__(self):
        return self.Medicine_name
