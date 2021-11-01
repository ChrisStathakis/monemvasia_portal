from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from .managers import CategoryManager


class Category(MPTTModel):
    is_featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=120, verbose_name='Τίτλος')

    content = models.TextField(blank=True, null=True, verbose_name='Σχόλια')
    timestamp = models.DateField(auto_now=True)
    meta_description = models.CharField(max_length=300, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Κατηγορία')

    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    objects = models.Manager()
    my_query = CategoryManager()

    class Meta:
        app_label = 'catalogue'
        verbose_name_plural = '3. Κατηγορίες Site'


    def save(self, *args, **kwargs):
        new_slug = slugify(self.name, allow_unicode=True)
        qs_exists = Category.objects.filter(slug=new_slug)
        self.slug = f'{new_slug}-{self.id}' if qs_exists.exists() else new_slug
        super().save()

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def front_name(self):
        full_path = [f'- {self.name}']
        k = self.parent
        while k is not None:
            space_sym = "&nbsp" * 4
            full_path.append(space_sym)
            k = k.parent
        return ''.join(full_path[::-1])

    def tag_active(self):
        return 'Is Active' if self.active else 'No active'

    def get_absolute_url(self):
        return reverse('product_category', kwargs={'slug': self.slug})

    def get_childrens(self):
        childrens = self.children.filter(active=True).order_by('order')
        return childrens

    @staticmethod
    def filter_data(queryset, request):
        search_name = request.GET.get('search_name', None)
        active_name = request.GET.getlist('active_name', None)
        menu_name = request.GET.getlist('menu_name', None)
        queryset = queryset.filter(name__icontains=search_name.capitalize()) if search_name else queryset
        queryset = queryset.filter(active=True) if active_name else queryset
        queryset = queryset.filter(show_on_menu=True) if 'a' in menu_name else queryset.filter(show_on_menu=False) if 'b' in menu_name else queryset
        return queryset
