from django.db import models

# Create your models here.


class Contact(models.Model):
    CHOICES = (
        ('a', 'ΓΕΝΙΚΗ ΕΡΩΤΗΣΗ'),
        ('b', 'ΓΙΑ ΕΠΙΧΕΙΡΗΣΕΙΣ')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CHOICES, max_length=1, default='a')
    email = models.EmailField()
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return f'{self.email}'


class BusinessContact(models.Model):

    PRIORITY_OPTIONS = (
        ('1', 'ΠΡΟΧΩΡΗΜΕΝΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 100/ΜΗΝΑ'),
        ('2', 'ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 40/ΜΗΝΑ'),
        ('3', 'ΒΑΣΙΚΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 20/ΜΗΝΑ')
    )
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
