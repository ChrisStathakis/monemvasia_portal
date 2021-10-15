from django import forms

from .models import CompanyInformation, Company, CompanyService, CompanyItems


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FrontEndCompanyInformationForm(BaseForm, forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = CompanyInformation
        fields = '__all__'


class CompanyServiceForm(BaseForm, forms.ModelForm):

    class Meta:
        model = CompanyService
        fields = '__all__'


class CompanyItemForm(BaseForm, forms.ModelForm):

    class Meta:
        model = CompanyItems
        fields = '__all__'