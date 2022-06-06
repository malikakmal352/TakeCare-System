from django.db import models
from Laboratory.models.Labcity import Labcity
from Doctor.models.All_Specialist import Special

# Create your models here.

class Doctor_request(models.Model):
    status = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    Doctor_name = models.CharField(max_length=200, default='')
    email = models.EmailField(default='')
    Gender = models.CharField(max_length=200, null=True, choices=gender, default='Male')
    Callnumber = models.BigIntegerField(default=1)
    city = models.CharField(max_length=100)
    Speciality = models.CharField(max_length=200, blank=True)
    Doctor_PMID_number = models.BigIntegerField(default=0)
    Status = models.CharField(max_length=20, null=True, choices=status, default='Pending')
    # Address = models.TextField(max_length=300, default="", blank=True, null=True)
    # Gender = models.CharField(max_length=20, null=True, choices=gender, default='Male')
    # forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_Accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.Doctor_name
