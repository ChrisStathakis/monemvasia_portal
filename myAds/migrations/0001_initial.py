# Generated by Django 3.2.7 on 2021-09-24 13:24

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('url', models.URLField(blank=True)),
                ('url_blank', models.BooleanField(default=False)),
                ('text', tinymce.models.HTMLField(blank=True)),
            ],
        ),
    ]
