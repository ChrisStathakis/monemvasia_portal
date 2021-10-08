# Generated by Django 3.2.3 on 2021-10-07 13:40

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_auto_20211007_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', tinymce.models.HTMLField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
            ],
        ),
    ]
