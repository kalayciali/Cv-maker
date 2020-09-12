from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from accounts.models import Profile
from . import models

class ExperienceForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = ('name', 'role', 'address', 'descript', 'start_date', 'end_date', 'decider')
        labels = {
            'name': "Ne deneyiminde bulundunuz? ya da Deneyimde bulunduğunuz yerin adı?",
            "role": "Sizin rolünüz ne idi?",
            "address": "Deneyimde bulunduğunuz yerin adresi",
            "descript": "Bu deneyimde neler yaptınız? Size katkıları ne oldu?",
            "start_date": "Başlama tarihi",
            "end_date": "Bitiş tarihi"
        }

ExperienceFormSet = inlineformset_factory(Profile, models.Experience, form=ExperienceForm, can_delete= False, extra=1)

class EducationForm(ModelForm):
    class Meta:
        model = models.Experience
        fields = ('name', 'role', 'descript', 'start_date', 'end_date', 'decider')
        labels = {
            "name": "Okul ya da Üniversite adı",
            "role": "Bölümünüz ve not ortalamanız",
            "descript": "Neler yaptığınız hakkında bahsetmek isterseniz?",
            "start_date": "Başlama tarihi",
            "end_date": "Bitiş tarihi"
        }

EducationFormSet = inlineformset_factory(Profile, models.Experience, form=EducationForm, can_delete= False,  extra=1)


class LangForm(ModelForm):
    class Meta:
        model = models.Bar
        fields = ('name', 'star', 'decider')
        labels = {
            'name': "Hangi dil",
            'star': "Ne kadar"
        }

LangFormSet= inlineformset_factory(Profile, models.Bar, form=LangForm, can_delete= False,  extra=1)

class TechForm(ModelForm):
    class Meta:
        model = models.Bar
        fields = ('name', 'star', 'decider')
        labels = {
            'name': "Hangi teknoloji",
            'star': "Ne kadar"
        }

TechFormSet= inlineformset_factory(Profile, models.Bar, form=TechForm, can_delete= False,   extra=1)

class SkillForm(ModelForm):
    class Meta:
        model = models.Bar
        fields = ('name', 'star', 'decider')
        labels = {
            'name': "Hangi yetenek",
            'star': "Ne kadar"
        }

SkillFormSet = inlineformset_factory(Profile, models.Bar, form=SkillForm, can_delete= False,   extra=1)

class AwardForm(ModelForm):
    class Meta:
        model = models.Award
        fields = ('name', 'date', 'decider')
        labels = {
            'name': "Ne ödülü aldınız? Hangi sertifika?",
            'date': "Hangi tarihte"
        }

AwardFormSet= inlineformset_factory(Profile, models.Award, form=AwardForm, can_delete= False,   extra=1)

class PublicForm(ModelForm):
    class Meta:
        model = models.Award
        fields = ('name', 'date', 'decider')
        labels = {
            'name': "Yayınınızın ismi",
            'date': "Hangi tarihte"
        }

PublicFormSet= inlineformset_factory(Profile, models.Award, form=PublicForm, can_delete= False,   extra=1)


class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = ('name', 'role', 'descript')
        labels = {
            "name": "Proje ismini yazınız.",
            "role": "Sizin rolünüz ne idi ya da Bir iki kelimeyle ana konuyu tanıtın.",
            "descript": "Neler yaptığınızı burada anlatabilirsiniz."
        }

ProjectFormSet= inlineformset_factory(Profile, models.Project, form=ProjectForm, can_delete= False,   extra=1)

