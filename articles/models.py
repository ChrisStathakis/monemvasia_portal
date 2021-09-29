from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse

from frontend.models import City
from .managers import CategoryManager, ArticleManager

from tinymce.models import HTMLField


class ArticleCategory(models.Model):
    have_children = models.BooleanField(default=False, verbose_name='Main Category')
    title = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=240, db_index=True)

    my_query = CategoryManager()
    objects = models.Manager()

    class Meta:
        ordering = ['-have_children', ]

    def save(self, *args, **kwargs):
        qs = ArticleCategory.objects.filter(parent=self)
        self.have_children = True if qs.exists() else False
        if not self.slug:
            new_slug = slugify(self.title, allow_unicode=True)
            qs_exists = ArticleCategory.objects.filter(slug=new_slug).exists()
            self.slug = f'{new_slug}-{self.id}' if qs_exists else new_slug
        super(ArticleCategory, self).save(*args, **kwargs)

    def main_articles(self):
        return self.articles.filter(publish=True, category_featured=True)

    def favorite_article(self):
        qs = self.articles.filter(publish=True, category_favorite=True)
        return qs.first() if qs.exists() else None

    def article_ad(self):
        qs = self.category_add.all()
        return qs.first() if qs.exists() else None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Article(models.Model):
    featured = models.BooleanField(default=False)
    category_favorite = models.BooleanField(default=False)
    category_featured = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    category = models.ManyToManyField(ArticleCategory, blank=True, related_name='articles')
    city = models.ManyToManyField(City, blank=True)
    title = models.CharField(max_length=240)
    text = HTMLField()
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=240, db_index=True)

    my_query = ArticleManager()
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title, allow_unicode=True)
            qs_exists = Article.objects.filter(slug=new_slug).exists()
            self.slug = f'{new_slug}-{self.id}' if qs_exists else new_slug
        super(Article, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})

    def image(self):
        qs = self.articlephotos_set.filter(is_primary=True)
        return qs.first().image if qs.exists() else None

    @staticmethod
    def filter_data(request, qs):
        return qs


def upload_articles(instance, filename):
    return f'articles/{instance.article.id}/{filename}'


class ArticlePhotos(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_articles)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.article.title} | {self.id}'
