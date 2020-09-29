from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from accounts.models import Profile
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class ExperienceForm(ModelForm):

    class Meta:
        model = models.Experience
        fields = ('name', 'role', 'address', 'descript', 'start_date', 'end_date')
        exclude = [ 'decider', ]
        labels = {
            'name': "Nerede? Firma adı?",
            "role": "Sizin rolünüz ne idi?",
            "address": "Şehir",
            "descript": "Bu deneyimde neler yaptınız? Size katkıları ne oldu?",
            "start_date": "Başlama tarihi",
            "end_date": "Bitiş tarihi"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('role', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('address', css_class='form-group col-md-2 mb-0'),
                Column('start_date', css_class='form-group col-md-2 mb-0'),
                Column('end_date', css_class='form-group col-md-2 mb-0'),
            ),
            Row(
                Column('descript', css_class='form-group col-md-6 mb-0'),
            ),
        )


ExperienceFormSet = inlineformset_factory(Profile, models.Experience, form=ExperienceForm, can_delete= False, extra=1)

class EducationForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = ('name', 'role', 'descript', 'start_date', 'end_date')
        exclude = [ 'decider', ]
        labels = {
            "name": "Okul ya da Üniversite adı",
            "role": "Bölümünüz ve not ortalamanız",
            "descript": "Neler yaptığınız hakkında bahsetmek isterseniz?",
            "start_date": "Başlama tarihi",
            "end_date": "Bitiş tarihi"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('role', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('start_date', css_class='form-group col-md-3 mb-0'),
                Column('end_date', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('descript', css_class='form-group col-md-6 mb-0'),
            ),
        )

EducationFormSet = inlineformset_factory(Profile, models.Experience, form=EducationForm, can_delete= False,  extra=1)


class LangForm(ModelForm):

    class Meta:
        model = models.Bar
        fields = ('name', 'star')
        exclude = [ 'decider', ]
        labels = {
            'name': "Hangi dil?",
            'star': "Ne kadar?"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('star', css_class='form-group col-md-3 mb-0'),
            ),
        )

LangFormSet= inlineformset_factory(Profile, models.Bar, form=LangForm, can_delete= False,  extra=1)

class TechForm(ModelForm):
    class Meta:
        model = models.Bar
        fields = ('name', 'star')
        exclude = [ 'decider', ]
        labels = {
            'name': "Hangi teknoloji?",
            'star': "Ne kadar?"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('star', css_class='form-group col-md-3 mb-0'),
            ),
        )

TechFormSet= inlineformset_factory(Profile, models.Bar, form=TechForm, can_delete= False,   extra=1)

class SkillForm(ModelForm):
    class Meta:
        model = models.Bar
        fields = ('name', 'star')
        exclude = [ 'decider', ]
        labels = {
            'name': "Hangi yetenek?",
            'star': "Ne kadar?"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('star', css_class='form-group col-md-3 mb-0'),
            ),
        )

SkillFormSet = inlineformset_factory(Profile, models.Bar, form=SkillForm, can_delete= False,   extra=1)

class AwardForm(ModelForm):
    class Meta:
        model = models.Award
        fields = ('name', 'date' )
        exclude = [ 'decider', ]
        labels = {
            'name': "Ne ödülü aldınız? Hangi sertifika?",
            'date': "Hangi tarihte?"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
            ),
        )

AwardFormSet= inlineformset_factory(Profile, models.Award, form=AwardForm, can_delete= False,   extra=1)

class PublicForm(ModelForm):
    class Meta:
        model = models.Award
        fields = ('name', 'date' )
        exclude = [ 'decider', ]
        labels = {
            'name': "Yayınınızın ismi",
            'date': "Hangi tarihte?"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('date', css_class='form-group col-md-3 mb-0'),
            ),
        )

PublicFormSet= inlineformset_factory(Profile, models.Award, form=PublicForm, can_delete= False,   extra=1)


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ('name', 'role', 'descript')
        labels = {
            "name": "Proje ismini yazınız.",
            "role": "Projenin ana konusu ?",
            "descript": "Neler yaptığınızı burada anlatabilirsiniz."
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('role', css_class='form-group col-md-3 mb-0'),
            ),
            Row(
                Column('descript', css_class='form-group col-md-6 mb-0'),
            ),
        )

ProjectFormSet= inlineformset_factory(Profile, models.Project, form=ProjectForm, can_delete= False,   extra=1)

