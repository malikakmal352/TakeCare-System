from django.db import models
from Doctor.models.Clinic import Clinic
from Laboratory.models.Labcity import Labcity
from Doctor.models.All_Specialist import Special


# Create your models here.

class Doctors(models.Model):
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    Doctor_name = models.CharField(max_length=200, default='')
    img = models.ImageField(upload_to='doctor_img/', default='', null=True, blank=True)
    Gender = models.CharField(max_length=200, null=True, choices=gender, default='Male')
    Experience = models.PositiveIntegerField(blank=True, default=0)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='', blank=True, null=True)
    Callnumber = models.BigIntegerField(default=1)
    city = models.CharField(max_length=100)
    Speciality = models.CharField(max_length=200)
    Doctor_PMID_number = models.BigIntegerField(default=0)
    Address = models.TextField(max_length=300, default="", blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    Doctor_Clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)
    Total_Reviews = models.PositiveIntegerField(default=0)
    Patient_satisfaction = models.PositiveBigIntegerField(default=0)
    satisfaction_per = models.PositiveBigIntegerField(default=0)

    # Satisfaction =
    is_Active = models.BooleanField(default=True)
    is_Live = models.BooleanField(default=False)


    def __str__(self):
        return self.Doctor_name

    def get_by_email(email):
        try:
            return Doctors.objects.get(email=email)
        except:
            return False

    def isExits(self):
        if Doctors.objects.filter(email=self.email):
            return True

        return False
