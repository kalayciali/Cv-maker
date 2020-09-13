from django.db import models
from accounts.models import Profile
from django.urls import reverse

# Create your models here.
class Cv(models.Model):
    name = models.CharField(max_length=100, blank=True)
    css = models.TextField(max_length=20000)
    html = models.TextField(max_length=20000, blank=True)
    loc_data = models.TextField(max_length=1000, blank=True)
    members = models.ManyToManyField(
        Profile,
        through='ProfileCv',
        through_fields=('cv', 'profile')
    )

class ProfileCv(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    new_html = models.TextField(max_length=20000, blank=True)

class Experience(models.Model):
    name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    descript = models.TextField(max_length=500, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    class DecideExp(models.TextChoices):
        EDUC = 'Ed'
        EXP = 'Exp'
    decider = models.CharField(choices=DecideExp.choices, max_length=5)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    class Meta:
        ordering = [ 'end_date' ]
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

class Bar(models.Model):
    name = models.CharField(max_length=100, blank=True)
    star = models.PositiveSmallIntegerField()
    class DecideBar(models.TextChoices):
        LANG = 'Lang'
        TECH = 'Tech'
        SKILL = 'Skill'
    decider = models.CharField(choices=DecideBar.choices, max_length=10)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Bar"
        verbose_name_plural = "Bars"


class Project(models.Model):
    name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    descript = models.TextField(max_length=500, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Award(models.Model):
    name = models.CharField(max_length=100, blank=True)
    date = models.DateField()
    class DecideAward(models.TextChoices):
        PUBLIC = 'Pub'
        AWARD = 'Award'
    decider = models.CharField(choices=DecideAward.choices, max_length=10)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Award"
        verbose_name_plural = "Awards"

