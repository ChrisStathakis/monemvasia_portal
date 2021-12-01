from django.db import models


class NewsLetter(models.Model):
    gender_types = (
        ('a', 'Άνδρας'),
        ('b', 'Γυναίκα'),
        ('c', 'Δε επιθυμώ να απαντήσω')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    approve = models.BooleanField(default=False, verbose_name='Αποδέχομαι τους όρους χρήσης')
    first_name = models.CharField(max_length=220, null=True, blank=True)
    last_name = models.CharField(max_length=220, null=True, blank=True)
    gender = models.CharField(choices=gender_types, max_length=1, default='c')

    def __str__(self):
        return self.title