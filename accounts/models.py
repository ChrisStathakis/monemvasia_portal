from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
User = get_user_model()

from companies.models import Company


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taxes_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    permission_grand = models.BooleanField(default=False)
    monthly_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


class InstagramCategories(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, verbose_name='ΤΙΤΛΟΣ')

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('accounts:edit_category', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('accounts:delete_link_or_category', kwargs={'action': 'category', 'pk': self.id})


class InstagramLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(InstagramCategories, on_delete=models.CASCADE, related_name='my_links', verbose_name='ΚΑΤΗΓΟΡΙΑ')
    title = models.CharField(max_length=200, verbose_name='ΤΙΤΛΟΣ')
    url = models.URLField()

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('accounts:edit_link', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('accounts:delete_link_or_category', kwargs={'action': 'link', 'pk': self.id})



