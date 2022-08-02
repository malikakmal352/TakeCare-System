from django.db import models


# Create your models here.

class Patient(models.Model):
    Cities = (
        ('Rawalpindi', 'Rawalpindi'),
        ('Islamabad', 'Islamabad'),
        ('Lahore', 'Lahore'),
        ('Karachi', 'Karachi'),
        ('Multan', 'Multan'),
    )

    name = models.CharField(max_length=200, default='')
    Mn = models.IntegerField(default=0)
    img = models.ImageField(upload_to='patient_img/', default='../static/deault_profile_image.png', blank=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=200, null=True, choices=Cities, default='Select your city')
    Address = models.TextField(max_length=300, default="", null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    is_Active = models.BooleanField(default=True)


    def __str__(self):
        return self.email

    # def delete(self, using=None, keep_parents=False):
    #     self.img.storage.delete(self.img.name)
    #     self.img.storage.delete(self.img.name)
    #     super().delete()

    def get_by_email(email):
        try:
            return Patient.objects.get(email=email)
        except:
            return False

    def isExits(self):
        if Patient.objects.filter(email=self.email):
            return True

        return False
