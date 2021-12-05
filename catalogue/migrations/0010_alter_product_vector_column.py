# Generated by Django 3.2.9 on 2021-12-04 07:14

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vector_column',
            field=django.contrib.postgres.search.SearchVectorField(blank=True, null=True),
        ),
    ]
