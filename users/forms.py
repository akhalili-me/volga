from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
))


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
