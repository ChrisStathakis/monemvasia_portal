from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from django.core.cache import cache
from .models import CompanyCategory, Company, CompanyInformation, CompanyImage, CompanyService

from monemvasia_portal.cache_keys import FEATURED_SERVICES, FEATURED_COMPANIES, NAVBAR_CATEGORIES


@receiver(post_save, sender=CompanyCategory)
def create_slug_for_category(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = CompanyCategory.objects.filter(slug=new_slug).exists()
        instance.slug = new_slug if not qs_exists else f'{new_slug}-{instance.id}'
        instance.save()


@receiver(post_save, sender=Company)
def create_slug_for_company(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Company.objects.filter(slug=new_slug).exists()
        instance.slug = new_slug if not qs_exists else f'{new_slug}-{instance.id}'
        instance.save()
    CompanyInformation.objects.get_or_create(company=instance)
    for service in instance.services.all():
        service.save()
    for product in instance.my_products.all():
        product.save()


@receiver(post_save, sender=CompanyImage)
def update_background_image(sender, instance, **kwargs):
    company = instance.company
    if instance.background_img:
        qs = company.images.filter(background_img=True).exclude(id=instance.id)
        qs.update(background_img=False)


@receiver(post_delete, sender=Company, dispatch_uid='company_deleted')
def refresh_cache_after_company_delete(sender, instance, **kwargs):
    if instance.featured:
        cache.delete(FEATURED_COMPANIES)


@receiver(post_save, sender=Company, dispatch_uid='company_updated')
def refresh_cache_after_company_updated(sender, instance, **kwargs):
    if instance.featured:
        cache.delete(FEATURED_COMPANIES)


@receiver(post_delete, sender=CompanyService, dispatch_uid='service_deleted')
def refresh_cache_after_service_delete(sender, instance, **kwargs):
    if instance.is_primary:
        cache.delete(FEATURED_SERVICES)


@receiver(post_save, sender=CompanyService, dispatch_uid='service_updated')
def refresh_cache_after_service_updated(sender, instance, **kwargs):
    if instance.is_primary:
        cache.delete(FEATURED_COMPANIES)


@receiver(post_save, sender=CompanyCategory, dispatch_uid='company_category_updated')
def refresh_cache_sfter_category_updated(sender, instance, **kwargs):
    cache.delete(NAVBAR_CATEGORIES)


@receiver(post_delete, sender=CompanyCategory, dispatch_uid='company_category_deleted')
def refresh_cache_after_category_deleted(sender, instance, **kwargs):
    cache.delete(NAVBAR_CATEGORIES)