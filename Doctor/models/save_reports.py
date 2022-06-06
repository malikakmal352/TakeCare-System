from mainpage.models.Patient import Patient
from django.db import models
from django.utils import timezone




# Create your models here.
class Save_Medical_Reports(models.Model):
    Reports = models.FileField(upload_to='Patient_save_Reports/',  default='', null=True, blank=True)
    Report_Title = models.CharField(max_length=200)
    Doctor_name = models.CharField(max_length=200)
    Patient_name = models.CharField(max_length=200)
    Date = models.DateField(default=timezone.now)
    Report_time = models.TimeField(blank=True)
    Note = models.TextField(blank=True)
    Patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.Report_Title

