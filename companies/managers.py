from django.db import models


class CompanyManager(models.Manager):

    def active(self):
        return self.filter(status=True)

    def normal_companies(self):
        return self.active().filter(featured=False)

    def featured(self):
        return self.active().filter(featured=True)

    def first_priority(self):
        return self.active().filter(priority='1')

    def first_choice(self):
        return self.active().filter(first_choice=True)


class ServiceManager(models.Manager):

    def subscribed(self):
        return self.filter(subscribe=True)

    def active(self):
        return self.filter(active=True)

    def is_primary(self):
        return self.filter(is_primary=True)
