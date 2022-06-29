from django.utils import timezone

from django.db import models
from Pharmacy_Store.models.Add_Medicine import Add_New_Medicine
from Pharmacy_Store.models.Add_pharmacy import Pharmacy
from mainpage.models.Patient import Patient


class order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Conform', 'Conform'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    PAYMENT = (
        ("Unpaid", "Unpaid"),
        ("Paid", "Paid"),
    )
    Medicine = models.ForeignKey(Add_New_Medicine, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, default=1)
    Pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default='')
    quantity = models.IntegerField()
    price = models.IntegerField()
    Total_price = models.IntegerField()
    Address = models.CharField(max_length=300, blank=True, default='')
    phone = models.BigIntegerField(blank=True, default='')
    payment = models.CharField(max_length=50, choices=PAYMENT, default='Unpaid')
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    product_status = models.BooleanField(default=True)
    is_Cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.Medicine.Medicine_name

    @staticmethod
    def get_orders_by_customer(id):
        # print(id)
        return order.objects.filter(Customer=id).order_by('-order_date')
