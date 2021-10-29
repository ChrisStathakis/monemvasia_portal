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
    title = models.CharField()
    text = models.TextField()


    def __str__(self):
        return f'{self.email}'


class BusinessContact(models.Model):
    email = models.EmailField()
    name = models.CharField()