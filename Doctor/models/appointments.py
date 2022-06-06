from datetime import datetime, timezone

from django.db import models
from Doctor.models.Clinic import Clinic
from mainpage.models.Patient import Patient
from Doctor.models.ADD_Docror import Doctors
from Doctor.models.save_reports import Save_Medical_Reports
from Laboratory.models.Labcity import Labcity
from Doctor.models.All_Specialist import Special


# Create your models here.

class Appointment(models.Model):
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    app_status = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Cancel', 'Cancel'),
        ('Completed', 'Completed'),
        ('Dispatch', 'Dispatch'),
    )
    # Patient_name = models.CharField(max_length=150)
    Name = models.CharField(default="", max_length=150)
    patient_phone = models.PositiveBigIntegerField(default=0)
    Gender = models.CharField(max_length=200, null=True, choices=gender, default='Male')
    Problem_detail = models.TextField(null=True, blank=True)

    Doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    Patients = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    Appointment_date = models.DateField(blank=True, null=True)
    Time_slot = models.TimeField(blank=True, null=True)
    time_start = models.CharField(max_length=100, null=True, blank=True)
    Status = models.CharField(max_length=20, choices=app_status, default='Pending')
    appointment_cancel_reason = models.TextField(max_length=300, null=True, default="", blank=True)
    Prescription = models.TextField(max_length=500, null=True, default="", blank=True)
    Medical_report_1 = models.ForeignKey(Save_Medical_Reports, on_delete=models.CASCADE, null=True, blank=True)
    # Report_2 = models.ForeignKey(Save_Medical_Reports, on_delete=models.CASCADE, null=True, blank=True)
    # Medical_report_3 = models.ForeignKey(Save_Medical_Reports, on_delete=models.CASCADE, null=True, blank=True)

    # Doctor_Clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Name
