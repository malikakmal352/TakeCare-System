# Generated by Django 4.0.4 on 2022-07-05 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(default='', max_length=200)),
                ('img', models.ImageField(blank=True, null=True, upload_to='lablogo/')),
                ('email', models.EmailField(default='', max_length=254)),
                ('password', models.CharField(default='', max_length=100)),
                ('Callnumber', models.BigIntegerField(blank=True, null=True)),
                ('Whatsapp', models.BigIntegerField(blank=True, null=True)),
                ('Address', models.TextField(default='', max_length=300)),
                ('forget_password_token', models.CharField(blank=True, max_length=100, null=True)),
                ('is_Active', models.BooleanField(default=True)),
            ],
        ),
    ]
