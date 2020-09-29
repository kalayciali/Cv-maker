from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('profile_pic', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-0'),
                Column('last_name', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('email', css_class='form-group col-md-3 mb-0'),
                Column('username', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('password1', css_class='form-group col-md-3 mb-0'),
                Column('password2', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('address', css_class='form-group col-md-3 mb-0'),
                Column('phone_num', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('links', css_class='form-group col-md-3 mb-0'),
                Column('bullet_descript', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('descript', css_class='form-group col-md-4 mb-0'),
            ),
            Submit('submit', 'Kaydol', css_class='btn btn-dark')
        )

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email','username',  'password1', 'password2', 'profile_pic' ,'bullet_descript', 'descript', 'phone_num', 'address', 'links')

class EditUserProfile(ModelForm):
    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-3 mb-0'),
                Column('last_name', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('email', css_class='form-group col-md-3 mb-0'),
            )
        )

class ProfileForm(ModelForm):
    class Meta():
        model = Profile
        fields = ('profile_pic' ,'bullet_descript', 'descript', 'phone_num', 'address', 'links')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('profile_pic', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('address', css_class='form-group col-md-3 mb-0'),
                Column('phone_num', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('links', css_class='form-group col-md-3 mb-0'),
                Column('bullet_descript', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('descript', css_class='form-group col-md-4 mb-0'),
            ),
            Submit('submit', 'Kaydol', css_class='btn btn-dark')
        )

