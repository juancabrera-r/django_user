from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

#Formulario que hereda de User (por defecto en django)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

#Formulario que hereda del modelo propio creado
class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')