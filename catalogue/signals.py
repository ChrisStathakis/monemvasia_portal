from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from monemvasia_portal.cache_keys import PRODUCT_CATEGORIES, FEATURED_PRODUCTS
from .models import Category, Product


@receiver(post_save, sender=Product, dispatch_uid='update_product')
def refresh_cache_after_products_updated(sender, instance, **kwargs):
    if instance.is_primary:
        cache.delete(FEATURED_PRODUCTS)


@receiver(post_delete, sender=Product, dispatch_uid='delete_product')
def refresh_cache_after_product_delete(sender, instance, **kwargs):
    if instance.is_primary:
        cache.delete(FEATURED_PRODUCTS)


@receiver(post_save, sender=Category, dispatch_uid='update_category')
def refresh_cache_after_products_updated(sender, instance, **kwargs):
    if instance.is_parent:
        cache.delete(PRODUCT_CATEGORIES)


@receiver(post_delete, sender=Category, dispatch_uid='delete_category')
def refresh_cache_after_product_delete(sender, instance, **kwargs):
    if instance.is_parent:
        cache.delete(PRODUCT_CATEGORIES)