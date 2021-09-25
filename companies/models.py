from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

from frontend.models import City


class Company(models.Model):
    status = models.BooleanField(default=False)
    item_support = models.BooleanField(default=False)
    max_items = models.IntegerField(default=6)
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title




class CompanyItems(models.Model):
    title =  models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    

    def __str__(self) -> str:
        return self.title