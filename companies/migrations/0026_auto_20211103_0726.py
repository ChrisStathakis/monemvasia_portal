# Generated by Django 3.2.8 on 2021-11-03 05:26

import companies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0025_auto_20211102_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['priority'], 'verbose_name_plural': '1. ΕΠΙΧΕΙΡΗΣΕΙΣ'},
        ),
        migrations.AlterModelOptions(
            name='companyimage',
            options={'verbose_name_plural': '2. ΕΙΚΟΝΕΣ ΕΠΙΧΕΙΡΗΣΕΩΝ'},
        ),
        migrations.AlterModelOptions(
            name='companyinformation',
            options={'verbose_name_plural': '2. ΠΡΟΦΙΛ ΕΠΙΧΕΙΡΗΣΕΩΝ'},
        ),
        migrations.AlterModelOptions(
            name='companyservice',
            options={'verbose_name': 'ΥΠΗΡΕΣΙΑ', 'verbose_name_plural': '4. ΥΠΗΡΕΣΙΕΣ'},
        ),
        migrations.RemoveField(
            model_name='companyinformation',
            name='small_image',
        ),
        migrations.AlterField(
            model_name='companyimage',
            name='image',
            field=models.ImageField(upload_to=companies.models.upload_image),
        ),
        migrations.AlterField(
            model_name='companyinformation',
            name='logo_image',
            field=models.ImageField(blank=True, upload_to=companies.models.upload_logo),
        ),
        migrations.AlterField(
            model_name='companyservice',
            name='image',
            field=models.ImageField(null=True, upload_to=companies.models.upload_services, verbose_name='ΕΙΚΟΝΑ'),
        ),
    ]
