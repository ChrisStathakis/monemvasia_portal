# Generated by Django 3.2.10 on 2022-02-28 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0041_auto_20220203_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='google_map_location',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]