# Generated by Django 3.1.6 on 2021-10-06 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_auto_20211005_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('background_image', models.ImageField(blank=True, help_text='1970*550', upload_to='')),
                ('logo_image', models.ImageField(blank=True, help_text='718*982', upload_to='')),
                ('small_image', models.ImageField(blank=True, help_text='247*232', upload_to='')),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('cellphone', models.CharField(blank=True, max_length=20)),
                ('website', models.URLField(blank=True)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='companies.company')),
            ],
        ),
    ]