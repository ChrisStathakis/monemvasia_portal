from django.db import models


class BannerManager(models.Manager):

    def active(self):
        return self.filter(active=True)

    def big_banner(self):
        return self.active().filter(category='a')

    def medium_banner(self):
        return self.active().filter(category='b')