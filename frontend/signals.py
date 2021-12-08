from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.core.cache import cache

from monemvasia_portal.cache_keys import CITIES, BIG_BANNERS_KEY, MEDIUM_BANNERS_KEY
from .models import City, Banner


@receiver(post_save, sender=City)
def create_slug_for_city(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = City.objects.filter(slug=new_slug).exists()
        instance.slug = new_slug if not qs_exists else f'{new_slug}-{instance.id}'
        instance.save()


@receiver(post_save, sender=City)
def refresh_cache_on_city_updated(sender, instance, **kwargs):
    cache.delete(CITIES)


@receiver(post_delete, sender=City)
def refresh_cache_on_city_deleted(sender, instance, **kwargs):
    cache.delete(CITIES)


@receiver(post_save, sender=Banner)
def refresh_cache_on_banner_updated(sender, instance, **kwargs):
    if instance.category == 'a':
        cache.delete(BIG_BANNERS_KEY)
    if instance.category == 'b':
        cache.delete(MEDIUM_BANNERS_KEY)


@receiver(post_delete, sender=Banner)
def refresh_cache_on_banner_delete(sender, instance, **kwargs):
    if instance.category == 'a':
        cache.delete(BIG_BANNERS_KEY)
    if instance.category == 'b':
        cache.delete(MEDIUM_BANNERS_KEY)