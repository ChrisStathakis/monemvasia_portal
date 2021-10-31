# Generated by Django 3.2.8 on 2021-10-31 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_readed', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=200, verbose_name='ΟΝΟΜΑΤΕΠΩΝΥΜΟ')),
                ('phone', models.CharField(max_length=15, verbose_name='ΤΗΛΕΦΩΝΟ ΕΠΙΚΟΙΝΩΝΙΑΣ')),
                ('afm', models.CharField(max_length=10, verbose_name='ΑΦΜ')),
                ('priority', models.CharField(choices=[('1', 'ΠΡΟΧΩΡΗΜΕΝΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 100/ΜΗΝΑ'), ('2', 'ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 40/ΜΗΝΑ'), ('3', 'ΒΑΣΙΚΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 20/ΜΗΝΑ')], default='3', max_length=1, verbose_name='ΠΛΑΝΟ')),
                ('city', models.CharField(max_length=150, verbose_name='ΠΟΛΗ')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('a', 'ΓΕΝΙΚΗ ΕΡΩΤΗΣΗ'), ('b', 'ΓΙΑ ΕΠΙΧΕΙΡΗΣΕΙΣ')], default='a', max_length=1)),
                ('email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
            ],
        ),
    ]
