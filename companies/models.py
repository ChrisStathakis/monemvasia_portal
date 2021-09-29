from django.db import models
from django.contrib.auth import get_user_model
from frontend.models import City


from tinymce.models import HTMLField
from .managers import CompanyManager

import datetime

User = get_user_model()


def upload_to(instance, filename):
    return f'/companies/{instance.title}/{filename}'


class Company(models.Model):
    PRIORITY_OPTIONS = (
        ('1', 'First. Subscription Cost:  50'),
        ('2', 'Second. Subscription Cost: 40'),
        ('3', 'Third. Subscription Cost:  30')
    )
    status = models.BooleanField(default=False)
    subscription_ends = models.DateField(null=True)
    image = models.ImageField(upload_to='companies/images/', help_text='400*400', null=True)
    logo = models.ImageField(upload_to='companies/logo/', null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default='3')
    item_support = models.BooleanField(default=False)
    max_items = models.IntegerField(default=6)
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    description = HTMLField(blank=True, null=True)

    my_query = CompanyManager()
    objects = models.Manager()

    counter = models.IntegerField(default=0)

    class Meta:
        ordering = ['priority', ]
        
    def save(self, *args, **kwargs):
        self.status = True if self.subscription_ends >= datetime.datetime.now().date() else False
        self.item_support = True if self.max_items > 0 else False
        super(Company, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class CompanyItems(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return self.title
