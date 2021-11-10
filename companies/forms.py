from django import forms

from .models import CompanyInformation, Company, CompanyService, CompanyImage


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FrontEndCompanyInformationForm(BaseForm, forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CompanyInformation
        fields = ['company', 'logo_image',
                  'address', 'phone', 'cellphone', 'website', 'email',
                  'description', 'facebook_url', 'instagram_url'

                  ]


class CompanyServiceForm(BaseForm, forms.ModelForm):

    class Meta:
        model = CompanyService
        fields = ['title', 'image', 'text', 'price']


class CompanyImageForm(BaseForm, forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput(), required=True)

    class Meta:
        model = CompanyImage
        fields = '__all__'
