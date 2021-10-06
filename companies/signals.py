from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify

from .models import CompanyCategory


@receiver(post_save, sender=CompanyCategory)
def create_slug_for_category(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = CompanyCategory.objects.filter(slug=new_slug).exists()
        instance.slug = new_slug if not qs_exists else f'{new_slug}-{instance.id}'
        instance.save()
