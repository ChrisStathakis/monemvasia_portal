from django.db import models

from tinymce.models import HTMLField

from .managers import MyAdsManager


class MyAd(models.Model):

    CATEGORIES = (
        ('a', 'Navbar Ad. Image size 728*90'),
        ('b', 'Main Ad')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    image = models.ImageField()
    title = models.CharField(unique=True, max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORIES, default='a')
    url = models.URLField(blank=True)
    url_blank = models.BooleanField(default=False)

    text = HTMLField(blank=True)
    count = models.IntegerField(default=0)

    objects = models.Manager()
    my_query = MyAdsManager()

    def __str__(self):
        return self.title