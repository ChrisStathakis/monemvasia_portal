from django.db import models


class CategoryManager(models.Manager):

    def parent_categories(self):
        return self.filter(parent__isnull=True)


class ArticleManager(models.Manager):

    def published(self):
        return self.filter(publish=True)

    def featured(self):
        return self.published().filter(featured=True)

