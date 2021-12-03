from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from catalogue.models import Product


def ajax_product_modal_view(request, slug):
    obj = get_object_or_404(Product, slug=slug)
    data = dict()
    data['result'] = render_to_string(
        template_name='ajax_views/product_modal.html',
        request=request,
        context={
            'obj': obj
        }
    )
    return JsonResponse(data)