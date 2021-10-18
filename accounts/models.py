from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taxes_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    permission_grand = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
