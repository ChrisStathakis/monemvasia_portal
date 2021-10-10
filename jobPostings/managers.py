from django.db import models


class JobPostingManager(models.Manager):

    def active(self):
        return self.filter(publish=True)

    def featured(self):
        return self.active().filter(featured=True)

    def filter_by_category(self, category):
        return self.active().filter(category=category)

