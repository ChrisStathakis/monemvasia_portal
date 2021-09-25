from django.db import models

# Create your models here.


class City(models.Model):
    title = models.CharField(unique=True, max_length=220)
    slug = models.SlugField(blank=True)

    def __str__(self) -> str:
        return self.title