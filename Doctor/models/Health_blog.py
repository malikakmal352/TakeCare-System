from django.db import models
# from django.forms import forms
from django.utils import timezone
from Doctor.models.ADD_Docror import Doctors


# Create your models here.

class Health_blogs(models.Model):
    Doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, null=True, blank=True)
    img = models.ImageField(upload_to='Health_blogs_img/', default='', null=True, blank=True)
    Blog_View = models.PositiveIntegerField(default=0)
    Health_blogs_issue = models.CharField(max_length=200, blank=True)
    Main_heading = models.CharField(max_length=200, blank=True)
    Health_blogs_Detail = models.TextField()
    # Related_to_Speciality = models.CharField(max_length=200)
    blog_create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Main_heading

    def delete(self, using=None, keep_parents=False):
        self.img.storage.delete(self.img.name)
        self.img.storage.delete(self.img.name)
        super().delete()
