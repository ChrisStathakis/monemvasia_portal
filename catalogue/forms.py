from django import forms

from .models import Product, Company


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'active':
                field.widget.attrs['class'] = 'my_class'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(BaseForm, forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput())


    class Meta:
        model = Product
        fields = ['active', 'title', 'company', 'image', 'category', 'text', 'sku', 'price', 'price_discount'
                  ]