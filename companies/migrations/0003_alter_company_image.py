# Generated by Django 3.2.3 on 2021-09-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_company_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(help_text='400*400', null=True, upload_to='companies'),
        ),
    ]
