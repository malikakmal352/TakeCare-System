from django.db import models
from django.forms import forms

from Laboratory.models.Labcity import Labcity
from Doctor.models.All_Specialist import Special



# Create your models here.

class Clinic(models.Model):
    Clinic_Name = models.CharField(max_length=200, default='')
    Doctor_email = models.EmailField(max_length=200, null=True, default="", blank=True)
    Location = models.CharField(max_length=200)
    Doctor_Fee = models.PositiveIntegerField(default=0, blank=True)
    Clinic_Number = models.PositiveIntegerField(default=1)
    # Patient_day = models.TimeField(default="00:05:00")
    Patient_day = models.PositiveIntegerField(default=5)
    # Time_per_Patients = models.
    Monday = models.BooleanField(default=True)
    clinic_time_start = models.TimeField(null=True, blank=True)
    clinic_time_end = models.TimeField(null=True, blank=True)

    Tuesday = models.BooleanField(default=True)
    Wednesday = models.BooleanField(default=True)
    Thursday = models.BooleanField(default=True)
    Friday = models.BooleanField(default=True)
    Saturday = models.BooleanField(default=False)
    Sunday = models.BooleanField(default=False)

    # Satisfaction =
    is_Active = models.BooleanField(default=True)

    def __str__(self):
        return self.Clinic_Name
