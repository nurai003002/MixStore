from django import forms
from django.contrib.auth.models import User

class EmailForm(forms.Form):
    email = forms.EmailField(label="Введите вашу почту", required=True)

class ResetPasswordForm(forms.Form):
    code = forms.CharField(label="Код, который был отправлен на ваш email", max_length=6, required=True)
    new_password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, required=True)