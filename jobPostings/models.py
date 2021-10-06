from django.db import models
from tinymce.models import HTMLField
# Create your models here.

from companies.models import Company
from .managers import  JobPostingManager


class JobCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'ΚΑΤΗΓΟΡΙΑ ΑΓΓΕΛΙΑΣ'
        verbose_name_plural = 'ΚΑΤΗΓΟΡΙΕΣ ΑΓΓΕΛΙΑΣ'

    def __str__(self):
        return self.title


class JobPost(models.Model):
    featured = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    text = HTMLField()
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    my_query = JobPostingManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'ΑΓΓΕΛΙΑ'
        verbose_name_plural = 'ΑΓΓΕΛΙΕΣ'

    def __str__(self):
        return self.title
