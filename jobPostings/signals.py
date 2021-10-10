from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify


from .models import JobCategory, JobPost


@receiver(post_save, sender=JobPost)
def create_slug_for_job_post(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title, allow_unicode=True)
        qs_exists = JobPost.objects.filter(slug=slug).exists()
        instance.slug = slug if not qs_exists else f'{slug}-{instance.id}'
        instance.save()


@receiver(post_save, sender=JobCategory)
def create_slug_for_job_post_category(sender, instance, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title, allow_unicode=True)
        qs_exists = JobCategory.objects.filter(slug=slug).exists()
        instance.slug = slug if not qs_exists else f'{slug}-{instance.id}'
        instance.save()