from django import forms
from .models import Book, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'translator',
                  'publish_year', 'category', 'image')


class SignupForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=30, min_length=3, required=True, help_text='الزامی')
    last_name = forms.CharField(
        max_length=50, min_length=3, required=True, help_text='الزامی')
    email = forms.EmailField(max_length=254, min_length=6,
                             required=True, help_text='الزامی')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2', 'email',)

    def claen(self):
        cleaned_date = super(SignupForm, self).clean()
        first_name = cleaned_date.get('first_name')
        last_name = cleaned_date.get('last_name')
        email = cleaned_date.get('email')
        username = cleaned_date.get('username')
        password1 = cleaned_date.get('password1')
        password2 = cleaned_date.get('password2')
        if not first_name and not last_name and not email and not username and not password1 and not password2:
            raise forms.ValidationError(
                'هیچ یک از فیلد ها نمیتوانند خالی باشند')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'telegram_id', 'tel_no')


class SearchForm(forms.Form):
    query = forms.CharField()
