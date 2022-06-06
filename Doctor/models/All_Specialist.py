from django.db import models


# Create your models here.
class Special(models.Model):
    Doctor_Speciality = models.CharField(max_length=100)
    img = models.FileField(upload_to='Doctors_Speciality_imgs/', blank=True, null=True)
    total_doctors = models.PositiveIntegerField(default=0)

    @staticmethod
    def get_all_Category():
        return Special.objects.all()

    def __str__(self):
        return self.Doctor_Speciality

    def delete(self, using=None, keep_parents=False):
        self.img.storage.delete(self.img.name)
        self.img.storage.delete(self.img.name)
        super().delete()