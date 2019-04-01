from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Given name')
    last_name = forms.CharField(max_length=30, required=True, help_text='Family name')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=30, required=True, help_text='username')

    BOOLEAN_CHOICES = ((True, 'Yes'), (False, 'No'))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, help_text='username')

    class Meta:
        model = User
        fields = (
            'username', 'password1',)
