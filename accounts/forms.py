from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    profile_pic = forms.ImageField()
    bullet_descript = forms.CharField(required= True, label="Sizi tanımlayan bir iki kelime")
    descript = forms.CharField( label="Kendinizi anlatın", required=True )
    phone_regex = RegexValidator(regex=r'^\d{11}$', message= "0 ile başlayarak 11 haneli olarak giriniz.")
    phone_num = forms.CharField(validators=[phone_regex, ], max_length=11, label="Başında 0 olan telefon no")
    address = forms.CharField(max_length=30, label="yaşadığınız şehir, ilçe")
    links = forms.CharField(max_length=100, label="links")

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_pic' ,'bullet_descript', 'descript', 'phone_num', 'address', 'links')

