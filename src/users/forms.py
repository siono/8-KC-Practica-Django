from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class LoginForm(forms.Form):

    login_username = forms.CharField(label="Username")
    login_password = forms.CharField(widget=forms.PasswordInput(), label="Password")

class UserForm(forms.Form):

    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    email = forms.EmailField(label='E-mail')
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Confirm your password',widget=forms.PasswordInput())
    blog_name = forms.CharField(label='Blog name')
    blog_description = forms.CharField(label='Blog description')

    def clean(self):
        existent_users = User.objects.filter(
            username=self.cleaned_data.get("username")
        )
        if len(existent_users) > 0 and self.instance not in existent_users:
            raise ValidationError('Username already exists')

        if self.cleaned_data.get("password") != self.cleaned_data.get("password_confirmation"):
            raise ValidationError("Passwords don't match")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'