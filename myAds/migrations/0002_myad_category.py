# Generated by Django 3.2.7 on 2021-09-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myad',
            name='category',
            field=models.CharField(choices=[('a', 'Navbar Ad. Image size 728*90'), ('b', 'Main Ad')], default='a', max_length=1),
        ),
    ]
