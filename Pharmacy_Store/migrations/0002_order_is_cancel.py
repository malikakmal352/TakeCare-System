# Generated by Django 4.0.4 on 2022-06-14 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pharmacy_Store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_Cancel',
            field=models.BooleanField(default=False),
        ),
    ]
