from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from mailing_list.forms import StyleFormMixin
from users.models import User


class RegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'phone', 'country', 'avatar')


class LoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserInputSecretKeyForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_input_secret_key',)


    def clean_user_input_secret_key(self):
        cleaned_data = self.cleaned_data.get('user_input_secret_key')
        if cleaned_data != self.instance.secret_key:
            raise forms.ValidationError('Неверный секретный ключ!')
        return cleaned_data

