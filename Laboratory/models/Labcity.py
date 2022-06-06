from django.db import models

# Create your models here.
class Labcity(models.Model):
    Lab_city_name = models.CharField(max_length=100)

    @staticmethod
    def get_all_Category():
        return Labcity.objects.all()

    def __str__(self):
        return self.Lab_city_name