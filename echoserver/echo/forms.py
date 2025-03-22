from django import forms
from .models import Book, User
from django.contrib.auth.forms import UserChangeForm

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'full_name', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in ['user', 'admin']:
            raise forms.ValidationError('Неверная роль')
        return role

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']