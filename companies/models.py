from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from frontend.models import City


from tinymce.models import HTMLField
from .managers import CompanyManager, ServiceManager

import datetime

User = get_user_model()

BUSINESS_TYPE = (
        ('1', 'ΕΜΠΟΡΙΟ'),
        ('2', 'ΕΣΤΙΑΣΗ'),
        ('3', 'ΥΠΗΡΕΣΙΕΣ'),
        ('4', 'ΜΕΙΚΤΟ')
    )


def upload_to(instance, filename):
    return f'/companies/images/{instance.id}/{filename}'


def upload_image(instance, filename):
    return f'/companies/images/{instance.company.id}/{filename}'


def upload_logo(instance, filename):
    return f'/companies/logos/{instance.company.id}/{filename}'


def upload_services(instance, filename):
    return f'/companies/services/{instance.company.id}/{filename}'


class CompanyCategory(models.Model):
    title = models.CharField(max_length=220)
    image = models.ImageField(upload_to='companies/categories/', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='childrens')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def have_childrens(self):
        return self.childrens.exists()

    def tag_image(self):
        return self.image.url if self.image else ''


class Company(models.Model):
    PRIORITY_OPTIONS = (
        ('1', 'ΠΡΟΧΩΡΗΜΕΝΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 100/ΜΗΝΑ'),
        ('2', 'ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 40/ΜΗΝΑ'),
        ('3', 'ΒΑΣΙΚΟ ΠΛΑΝΟ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 20/ΜΗΝΑ')
    )

    business_type = models.CharField(choices=BUSINESS_TYPE, default='1', max_length=1)
    featured = models.BooleanField(default=False)
    first_choice = models.BooleanField(default=False)
    category = models.ManyToManyField(CompanyCategory, null=True, blank=True)
    status = models.BooleanField(default=False)
    subscription_ends = models.DateField(null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default='3')
    item_support = models.BooleanField(default=False)
    max_items = models.IntegerField(default=6)
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='companies')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    google_map_location = models.URLField(blank=True, null=True, max_length=1000)

    # page_relates_fields
    service_title = models.CharField(max_length=220, default='ΥΠΗΡΕΣΙΕΣ')

    my_query = CompanyManager()
    objects = models.Manager()

    counter = models.IntegerField(default=0)

    class Meta:
        ordering = ['priority', ]
        verbose_name_plural = '1. ΕΠΙΧΕΙΡΗΣΕΙΣ'
        
    def save(self, *args, **kwargs):
        self.status = True if self.subscription_ends >= datetime.datetime.now().date() else False
        self.item_support = True if self.max_items > 0 else False
        super(Company, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('company_view', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('accounts:update_company_info', kwargs={'slug': self.slug})

    def support_products(self):
        return True if self.business_type in ['1', '4'] else False

    def support_service(self)-> bool:
        return True if self.business_type in ['3', '4'] else False

    def sub_value(self):
        return 20 if self.business_type == '3' else 40 if self.business_type == '2' else 100

    def get_background_image(self):
        qs = self.images.filter(background_img=True)
        return qs.first().image.url if qs.exists() else None

    def rest_photos(self):
        return self.images.filter(background_img=False)


    @staticmethod
    def filter_data(request, qs):
        q = request.GET.get('q', None)
        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(city__title__icontains=q)
                           )
        return qs


class CompanyInformation(models.Model):
    is_visible = models.BooleanField(default=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='detail')
    logo_image = models.ImageField(blank=True, upload_to='companies/logos/')
    address = models.CharField(blank=True, verbose_name='ΔΙΕΥΘΥΝΣΗ', max_length=220)
    phone = models.CharField(max_length=20, blank=True, verbose_name='ΤΗΛΕΦΩΝΟ')
    cellphone = models.CharField(max_length=20, blank=True, verbose_name='ΚΙΝΗΤΟ')
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True, null=True)
    description = HTMLField(blank=True, null=True, verbose_name='ΠΕΡΙΓΡΑΦΗ')
    facebook_url = models.URLField(blank=True, null=True, verbose_name='ΣΕΛΙΔΑ FACEBOOK')
    instagram_url = models.URLField(blank=True, null=True, verbose_name='ΣΕΛΙΔΑ INSTAGRAM')

    class Meta:
        verbose_name_plural = '2. ΠΡΟΦΙΛ ΕΠΙΧΕΙΡΗΣΕΩΝ'

    def __str__(self):
        return self.company.title

    def full_phones(self):
        phones = self.cellphone if self.cellphone else ''
        phones += f' | {self.phone}' if self.phone else '.'
        return phones

    def full_address(self):
        return f'{self.address} | {self.company.city}'

    def tag_image(self):
        return self.logo_image.url if self.logo_image else ''



class CompanyImage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='companies/images/')
    background_img = models.BooleanField(default=False, verbose_name='ΕΞΩΦΥΛΛΟ')

    class Meta:
        verbose_name_plural = '2. ΕΙΚΟΝΕΣ ΕΠΙΧΕΙΡΗΣΕΩΝ'

    def get_edit_url(self):
        return reverse('accounts:update_company_image', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('accounts:delete_company_image', kwargs={'pk': self.pk})




class CompanyService(models.Model):
    active = models.BooleanField(default=True)
    subscribe = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to='companies/service/images/', verbose_name='ΕΙΚΟΝΑ', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=250, verbose_name='ΤΙΤΛΟΣ')
    text = HTMLField(verbose_name='ΠΕΡΙΓΡΑΦΗ')
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='ΤΙΜΗ')

    objects = models.Manager()
    my_query = ServiceManager()

    class Meta:
        verbose_name_plural = '4. ΥΠΗΡΕΣΙΕΣ'
        verbose_name = 'ΥΠΗΡΕΣΙΑ'

    def save(self, *args, **kwargs):
        self.subscribe = self.company.status
        super(CompanyService, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('company:service_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('company:service-delete', kwargs={'pk': self.id})

    def tag_primary(self):
        return 'ΕΧΕΙ ΠΡΟΤΕΡΙΟΤΗΤΑ' if self.is_primary else 'ΔΕ ΕΧΕΙ'

    def tag_image(self):
        return self.image.url if self.image else ''

    def get_detail_url(self):
        return reverse('company_view', kwargs={'slug': self.company.slug})

    @staticmethod
    def filter_data(request, qs):
        q = request.GET.get('q', None)
        qs = qs.filter(title__icontains=q) if q else qs
        return qs