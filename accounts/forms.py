from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    profile_pic = forms.ImageField(label="Profil fotoğrafınız")
    bullet_descript = forms.CharField(required= True, label="Sizi vurgulayan bir iki kelime", widget=forms.TextInput(attrs= {
        'placeholder': 'Kimya Mühendisi, Teknisyen..'
    }))
    descript = forms.CharField( label="Kendinizi anlatın", required=True, widget=forms.Textarea)
    phone_regex = RegexValidator(regex=r'^\d{11}$', message= "0 ile başlayarak 11 haneli olarak giriniz.")
    phone_num = forms.CharField(validators=[phone_regex, ], max_length=11, label="0 dahil telefon numaranız")
    address = forms.CharField(max_length=30, label="yaşadığınız şehir, ilçe")
    links = forms.CharField(max_length=200, label="Sosyal hesaplarınız", widget=forms.Textarea(attrs = {
        'placeholder': """www.linkedin.com/in/username/
www.twitter.com/username""",
    }) )

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email','username',  'password1', 'password2', 'profile_pic' ,'bullet_descript', 'descript', 'phone_num', 'address', 'links')

class EditUserProfile(ModelForm):
    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name')

class ProfileForm(ModelForm):
    class Meta():
        model = Profile
        fields = ('profile_pic' ,'bullet_descript', 'descript', 'phone_num', 'address', 'links')

