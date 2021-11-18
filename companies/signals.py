from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify

from .models import CompanyCategory, Company, CompanyInformation, CompanyImage


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
