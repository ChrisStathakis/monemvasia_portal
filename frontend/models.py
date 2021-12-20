from django.db import models
from django.shortcuts import reverse
from tinymce.models import HTMLField
# Create your models here.

from .managers import BannerManager


class City(models.Model):
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='cities/', help_text='1370*385')
    title = models.CharField(unique=True, max_length=220)
    slug = models.SlugField(blank=True, allow_unicode=True)
    text = HTMLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'slug': self.slug})

    def tag_image(self):
        return self.image.url if self.image else None

class Banner(models.Model):
    choices = (
        ('a', 'Big Banner'),
        ('b', 'Medium Banner')
    )
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=220)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/', )
    url = models.URLField(blank=True)
    category = models.CharField(default='a', choices=choices, max_length=1)

    objects = models.Manager()
    my_query = BannerManager()

    def __str__(self):
        return self.title
