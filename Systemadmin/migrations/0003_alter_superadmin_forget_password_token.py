# Generated by Django 3.2.5 on 2022-02-13 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Systemadmin', '0002_alter_superadmin_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superadmin',
            name='forget_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
