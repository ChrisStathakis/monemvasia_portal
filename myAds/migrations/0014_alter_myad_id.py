# Generated by Django 3.2.8 on 2021-10-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAds', '0013_auto_20211014_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myad',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]