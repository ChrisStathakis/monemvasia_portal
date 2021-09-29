from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_fee = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f'Profile {self.user}'