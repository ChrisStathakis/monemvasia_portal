from django import forms
from django.contrib.auth.forms import UserCreationForm

from companies.forms import BaseForm
from .models import User, Profile


class LoginForm(BaseForm):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class UserCreationCustomForm(BaseForm, UserCreationForm):
    taxes_id = forms.CharField(required=True, label='ΑΦΜ')
    name = forms.CharField(required=False, label='ΟΝΟΜΑΤΕΠΩΝΥΜΟ')
    username = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'taxes_id', 'name', 'password1', 'password2']

    def clean_username(self):
        cleaned_data = self.cleaned_data.get('username', '')
        if not '@' in cleaned_data:
            return forms.ValidationError('Το Email που χρησιμοποίεισατε έχει λάθος συντάξη.')
        qs = User.objects.filter(username=cleaned_data)
        if qs.exists():
            return forms.ValidationError('Το Email χρησιμοποιειται ήδη. Δοκιμάστε κάποιο άλλο.')
        return cleaned_data

    def clean_taxes_id(self):
        cleaned_data = self.cleaned_data.get('taxes_id', '')
        qs = Profile.objects.filter(taxes_id=cleaned_data)
        if qs.exists():
            return forms.ValidationError('Το ΑΦΜ χρησιμοποιείται ήδη, Παρακαλώ εποικινονήστε με τους διαχειριστές.')
        return cleaned_data


class ProfileForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
