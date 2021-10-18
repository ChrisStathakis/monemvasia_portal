from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from frontend.models import City


from tinymce.models import HTMLField
from .managers import CompanyManager

import datetime

User = get_user_model()

BUSINESS_TYPE = (
        ('1', 'ΕΜΠΟΡΙΟ'),
        ('2', 'ΕΣΤΙΑΣΗ'),
        ('3', 'ΥΠΗΡΕΣΙΕΣ'),
        ('4', 'ΜΕΙΚΤΟ')
    )


def upload_to(instance, filename):
    return f'/companies/{instance.title}/{filename}'


class CompanyCategory(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='childrens')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def have_childrens(self):
        return self.childrens.exists()


class Company(models.Model):
    PRIORITY_OPTIONS = (
        ('1', 'First. Subscription Cost:  50'),
        ('2', 'Second. Subscription Cost: 40'),
        ('3', 'Third. Subscription Cost:  30')
    )

    business_type = models.CharField(choices=BUSINESS_TYPE, default='1', max_length=1)
    featured = models.BooleanField(default=False)
    first_choice = models.BooleanField(default=False)
    category = models.ManyToManyField(CompanyCategory, null=True, blank=True)
    status = models.BooleanField(default=False)
    subscription_ends = models.DateField(null=True)
    logo = models.ImageField(upload_to='companies/logo/', null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default='3')
    item_support = models.BooleanField(default=False)
    max_items = models.IntegerField(default=6)
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='companies')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

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

    def get_absolute_url(self):
        return reverse('company_view', kwargs={'slug': self.slug})

    @staticmethod
    def filter_data(request, qs):
        return qs


class CompanyInformation(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='detail')
    background_image = models.ImageField(help_text='1970*550', blank=True)
    logo_image = models.ImageField(help_text='718*982', blank=True)
    small_image = models.ImageField(help_text='247*232', blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    cellphone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company.title


class CompanyItems(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(help_text='400*400', upload_to='products')
    text = HTMLField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = 'ΠΡΟΪΟΝΤΑ'
        verbose_name = 'ΠΡΟΪΟΝ'

    def __str__(self) -> str:
        return self.title


class CompanyService(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=250)
    text = HTMLField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = 'ΥΠΗΡΕΣΙΕΣ'
        verbose_name = 'ΥΠΗΡΕΣΙΑ'

    def __str__(self):
        return self.title

