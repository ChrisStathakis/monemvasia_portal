from django.db import models
from django.shortcuts import reverse
from tinymce.models import HTMLField
# Create your models here.


class City(models.Model):
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='cities/')
    title = models.CharField(unique=True, max_length=220)
    slug = models.SlugField(blank=True, allow_unicode=True)
    text = HTMLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'slug': self.slug})


class Banner(models.Model):
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=220)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/', )
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title