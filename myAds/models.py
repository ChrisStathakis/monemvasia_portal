from django.db import models

from tinymce.models import HTMLField

from .managers import MyAdsManager


def upload_ad(instance, filename):
    print(filename)
    return f'/adds/{instance.id}/{filename}'


class MyAd(models.Model):

    CATEGORIES = (
        ('a', 'Navbar Ads. Image size 728*90'),
        ('b', 'Main Ads'),
        ('c', 'Page Ads'),
        ('d', 'Category Ads')
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    image = models.ImageField(upload_to='my_adds/%Y/%m/%d/')
    title = models.CharField(unique=True, max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORIES, default='a')
    article_category = models.ForeignKey('articles.ArticleCategory', blank=True, null=True, on_delete=models.SET_NULL, related_name='category_add')
    url = models.URLField(blank=True)
    url_blank = models.BooleanField(default=False)

    text = HTMLField(blank=True)
    count = models.IntegerField(default=0)

    objects = models.Manager()
    my_query = MyAdsManager()

    def __str__(self):
        return self.title
