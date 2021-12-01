from django import forms

from .models import NewsLetter


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewsLetterFrontEndForm(forms.ModelForm):

    class Meta:
        model = NewsLetter
        fields = ['email', 'approve']