from django import forms

from .models import Contact


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            pass


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['title', 'email', 'category', 'text' ]
