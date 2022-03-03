# Generated by Django 3.2.10 on 2022-03-03 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_auto_20220303_0806'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyservice',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='category_services', to='catalogue.ServiceCategory'),
        ),
    ]
