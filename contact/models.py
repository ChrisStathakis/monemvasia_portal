from django.db import models

# Create your models here.

from companies.models import PRIORITY_OPTIONS

class Contact(models.Model):
    CHOICES = (
        ('a', 'ΓΕΝΙΚΗ ΕΡΩΤΗΣΗ'),
        ('b', 'ΓΙΑ ΕΠΙΧΕΙΡΗΣΕΙΣ')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CHOICES, max_length=1, default='a', verbose_name='ΚΑΤΗΓΟΡΙΑ')
    email = models.EmailField()
    title = models.CharField(max_length=200, verbose_name='ΤΙΤΛΟΣ')
    text = models.TextField(verbose_name='ΠΕΡΙΓΡΑΦΗ')

    def __str__(self):
        return f'{self.email}'


class BusinessContact(models.Model):


    is_readed = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, verbose_name='ΟΝΟΜΑΤΕΠΩΝΥΜΟ')
    title = models.CharField(max_length=200, verbose_name='ONOMA ΕΤΑΙΡΙΑΣ')
    phone = models.CharField(max_length=15, verbose_name='ΤΗΛΕΦΩΝΟ ΕΠΙΚΟΙΝΩΝΙΑΣ')
    afm = models.CharField(max_length=10, verbose_name='ΑΦΜ', unique=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS,
                                default='3', verbose_name='ΠΛΑΝΟ')
    city = models.CharField(max_length=150, verbose_name='ΠΟΛΗ')

    class Meta:
        verbose_name_plural = 'ΕΓΓΡΑΦΕΣ ΕΠΙΧΕΙΡΗΣΕΩΝ'

    def __str__(self):
        return self.name
