# Generated by Django 3.1.6 on 2021-10-06 14:05

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('jobPostings', '0002_auto_20211005_1601'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='jobpost',
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
    ]