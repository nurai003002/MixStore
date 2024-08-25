from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class EmailForm(forms.Form):
    email = forms.EmailField(label="Введите вашу почту", required=True)

class ResetPasswordForm(forms.Form):
    code = forms.CharField(max_length=6)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Проверка сложности пароля
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError("Пароли не совпадают.")
        return cleaned_data