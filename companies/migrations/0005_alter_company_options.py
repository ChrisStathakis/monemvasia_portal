# Generated by Django 3.2.3 on 2021-09-28 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20210928_0743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['priority']},
        ),
    ]
