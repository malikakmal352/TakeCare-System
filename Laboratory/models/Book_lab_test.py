from datetime import datetime, date

from django.db import models
from mainpage.models.Patient import Patient
from Laboratory.models.Labcity import Labcity
from Laboratory.models.Lab_tests_list import Test_list
from Laboratory.models.add_lab import Lab
from Laboratory.models.Samplest import Samplest


# Create your models here.

class Book_Test(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Conform', 'Conform'),
        ('Sample Collected', 'Sample Collected'),
        ('Test Report', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Dispatch', 'Dispatch'),

    )
    Test_type = (
        ('home sample', 'home sample'),
        ('Lab Visit', 'Lab Visit'),
    )
    pay = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )

    Patient_Name = models.CharField(max_length=100, default='')
    email = models.ForeignKey(Patient, on_delete=models.CASCADE, default="")
    city = models.CharField(max_length=100, default='', blank=True)
    Phone = models.BigIntegerField(default=0, blank=True)
    Address = models.TextField(max_length=300, default="")
    Laboratory = models.ForeignKey(Lab, on_delete=models.CASCADE, default=1)
    Book_Test = models.ForeignKey(Test_list, on_delete=models.CASCADE, default=1)
    Test_date = models.DateField(default=date.today, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')
    payment = models.CharField(max_length=50, null=True, choices=pay, default='Pending')

    Test_Type = models.CharField(max_length=200, null=True, choices=Test_type, default='Lab Visit')
    Test_report = models.FileField(upload_to='Test Reports/', default='', null=True, blank=True)

    Samplest = models.ForeignKey(Samplest, on_delete=models.CASCADE, blank=True, null=True)

    year = models.CharField(max_length=100, blank=True, default=datetime.now().year)
    month = models.CharField(max_length=100, blank=True, default=datetime.now().month)

    # Bill = models.ForeignKey(Test_list.)

    def __str__(self):
        return self.Patient_Name
