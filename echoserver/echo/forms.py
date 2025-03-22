from django import forms
from .models import Book, User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'full_name', 'role']

    # Поля для ввода паролей
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
