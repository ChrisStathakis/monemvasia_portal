from django.db import models


class CategoryManager(models.Manager):

    def parent_categories(self):
        return self.filter(parent__isnull=True)