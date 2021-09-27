from django.db import models
from tinymce.models import HTMLField
# Create your models here.

from companies.models import Company


class JobCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)


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
