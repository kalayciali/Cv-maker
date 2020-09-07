from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from accounts.models import Profile

# Create your views here.

def manage_cv(request):
    profile = request.user.profile
    if request.method == "POST":
        all_formsets = generate_formsets(request)
        with transaction.atomic():
            if valid_for(all_formsets):
                return_after_saving(all_formsets)
                return redirect('select-cv')
    else:
        all_formsets = generate_formsets(request)
        return render(request, 'cvs/manage_cv.html', {
            'all_formsets': all_formsets
        })

# Helper functions

def generate_formsets(request):
    profile = request.user.profile
    all_formsets = []
    if request.method == "POST":
        exp_formset = forms.ExperienceFormSet(request.POST, instance=profile, prefix='experiences')
        all_formsets.append(exp_formset)

        ed_formset = forms.EducationFormSet(request.POST, instance=profile, prefix='educations')
        all_formsets.append(ed_formset)

        lang_formset = forms.LangFormSet(request.POST, instance=profile, prefix='languages')
        all_formsets.append(lang_formset)

        tech_formset = forms.TechFormSet(request.POST, instance=profile, prefix='techs')
        all_formsets.append(tech_formset)

        skill_formset = forms.SkillFormSet(request.POST, instance=profile, prefix='skills')
        all_formsets.append(skill_formset)

        award_formset = forms.AwardFormSet(request.POST, instance=profile, prefix='awards')
        all_formsets.append(award_formset)

        public_formset = forms.PublicFormSet(request.POST, instance=profile, prefix="publications")
        all_formsets.append(public_formset)

        project_formset = forms.ProjectFormSet(request.POST, instance=profile, prefix="projects")
        all_formsets.append(project_formset)

    else:
        exp_formset = forms.ExperienceFormSet( instance=profile, prefix='experiences', initial= [
            {'decider': 'Exp',}
        ])
        all_formsets.append(exp_formset)

        ed_formset = forms.EducationFormSet( instance=profile, prefix='educations', initial= [
            { 'decider': 'Ed',}
        ])
        all_formsets.append(ed_formset)

        lang_formset = forms.LangFormSet( instance=profile, prefix='languages', initial=[
            { 'decider': 'Lang', }
        ])
        all_formsets.append(lang_formset)

        tech_formset = forms.TechFormSet( instance=profile, prefix='techs', initial=[
            { 'decider': 'Tech', }
        ])
        all_formsets.append(tech_formset)

        skill_formset = forms.SkillFormSet( instance=profile, prefix='skills', initial=[
            { 'decider': 'Skill', }
        ])
        all_formsets.append(skill_formset)

        award_formset = forms.AwardFormSet( instance=profile, prefix='awards', initial=[
            { 'decider': 'Award' }
        ])
        all_formsets.append(award_formset)

        public_formset = forms.PublicFormSet( instance=profile, prefix="publications", initial=[
            { 'decider': 'Pub' }
        ])
        all_formsets.append(public_formset)

        project_formset = forms.ProjectFormSet( instance=profile, prefix="projects")
        all_formsets.append(project_formset)

    return all_formsets

def valid_for(formsets):
    for formset in formsets:
        if not formset.is_valid():
            return False
    return True

def return_after_saving(formsets):
    for formset in formsets:
        formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save()


