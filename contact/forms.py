from django import forms

from .models import Contact, BusinessContact


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ContactForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['title', 'email', 'category', 'text' ]


class BusinessContactForm(BaseForm, forms.ModelForm):

    class Meta:
        model = BusinessContact
        fields = '__all__'
        exclude = ['is_readed', ]