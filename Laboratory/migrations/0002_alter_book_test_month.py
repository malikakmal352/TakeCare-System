# Generated by Django 4.0.4 on 2022-08-01 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Laboratory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_test',
            name='month',
            field=models.CharField(blank=True, default=8, max_length=100),
        ),
    ]
