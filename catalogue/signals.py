from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify


from monemvasia_portal.cache_keys import PRODUCT_CATEGORIES, FEATURED_PRODUCTS
from .models import Category, Product


@receiver(post_save, sender=Product)
def create_slug_for_product(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Product.objects.filter(slug=new_slug).exists()
        instance.slug = f'{new_slug}-{instance.id}' if qs_exists else new_slug
        instance.save()


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