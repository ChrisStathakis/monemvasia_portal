from django.db import models


class CompanyManager(models.Manager):

    def active(self):
        return self.filter(status=True)

    def featured(self):
        return self.active().filter(featured=True)

    def first_priority(self):
        return self.active().filter(priority='1')

    def first_choice(self):
        return self.active().filter(first_choice=True)