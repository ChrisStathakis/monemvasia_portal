# Generated by Django 3.2.8 on 2022-01-10 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_producthitcounter'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
