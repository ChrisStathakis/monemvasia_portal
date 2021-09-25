from django.db import models


class MyAdsManager(models.Manager):

    def active(self):
        return self.filter(active=True)

    def navbar_ads(self):
        return self.active().filter(category='a')[:3]
