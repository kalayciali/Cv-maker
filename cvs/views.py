from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from accounts.models import Profile
from django.http import HttpResponse
import json
import re
from collections import OrderedDict

# Create your views here.

def manage_cv(request):
    profile = request.user.profile
    if request.method == "POST":
        all_formsets = generate_formsets(request)
        with transaction.atomic():
            if valid_for(all_formsets):
                return_after_saving(all_formsets)
                return redirect(showCv)
            else:
                errs = []
                for formset in all_formsets:
                    errs.append(formset.errors)
                return redirect('showCv', prof=profile)
    else:
        all_formsets = generate_formsets(request)
        return render(request, 'cvs/manage_cv.html', {
            'all_formsets': all_formsets
        })

def index_cvs(request):
    profile = request.user.profile
    if request.method == "POST":
        pass
    else:
        cv = models.Cv.objects.all()[0]
        newHtml = generateHtml(cv.loc_data, cv, profile)
        prof_cv = models.ProfileCv(profile=profile, cv=cv, new_html=newHtml)
        prof_cv.save()
        return HttpResponse(newHtml)
        # return render(request, 'cvs/show_cv.html', { 'newHtml': newHtml })

# Helper functions

def generateHtml(locData, cv, prof):
    loc_data = json.loads(locData, object_pairs_hook=OrderedDict)
    keys = list(loc_data.keys())
    # locations as list [[start_idx, end_idx], ..]
    locs = list(loc_data.values())
    html_temp = cv.html
    new_html_list = []
    old_loc = 0

    bar_locs = []
    link_locs = []
    exp_locs = []
    educ_locs = []
    bars = None
    links = None
    exps = None
    educs = None


    for i in range(len(keys)):

        capture = keys[i]
        substit = genRequiredFieldFrom(cv, prof, capture)
        loc = locs[i]

        if (capture == "hum_bar" or "bar_" in capture ):
            if capture == "hum_bar":
                bars = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)

            bar_locs.append(loc)
            # continue until bars finished
            continue

        if bars:
            for title in bars.keys():
                appendCharTo(new_html_list, bar_locs[0][0], bar_locs[1][0], html_temp)
                appendAfterGen(new_html_list, title)
                appendCharTo(new_html_list, bar_locs[1][1], bar_locs[2][0], html_temp)
                for bar in bars[title]:
                    appendCharTo(new_html_list, bar_locs[2][0], bar_locs[3][0], html_temp)
                    appendAfterGen(new_html_list, bar.name)
                    appendCharTo(new_html_list, bar_locs[3][1], bar_locs[4][0], html_temp)
                    appendAfterGen(new_html_list, f"width: {bar.star}%;")
                    appendCharTo(new_html_list, bar_locs[4][1], bar_locs[5][0], html_temp)
                    appendAfterGen(new_html_list, f"{bar.star}%")
                    appendCharTo(new_html_list, bar_locs[5][1], bar_locs[2][1], html_temp)
                appendCharTo(new_html_list, bar_locs[2][1], bar_locs[0][1], html_temp)
            old_loc = bar_locs[0][1]
            bars = None

        if (capture == "link_item" or "link_" in capture):
            if capture == "link_item":
                links = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            link_locs.append(loc)
            continue

        if links:
            names = links["name"]
            ids = links["id"]
            for i in range(len(names)):
                appendCharTo(new_html_list, link_locs[0][0], link_locs[1][0], html_temp)
                appendAllSrcTo(new_html_list, linkStyle(names[i]))
                appendCharTo(new_html_list, link_locs[1][1], link_locs[2][0], html_temp)
                appendAfterGen(new_html_list, names[i])
                appendCharTo(new_html_list, link_locs[2][1], link_locs[3][0], html_temp)
                appendAfterGen(new_html_list, ids[i])
                appendCharTo(new_html_list, link_locs[3][1], link_locs[0][1], html_temp)
            old_loc = link_locs[0][1]
            links = None

        if (capture == "exp_item" or "exp_" in capture):
            if capture == "exp_item":
                exps = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            exp_locs.append(loc)
            continue

        if exps:
            for exp in exps:
                appendCharTo(new_html_list, exp_locs[0][0], exp_locs[1][0], html_temp)
                appendAfterGen(new_html_list, f"{exp.start_date}--{exp.end_date}")
                appendCharTo(new_html_list, exp_locs[1][1], exp_locs[2][0], html_temp)
                appendAfterGen(new_html_list, exp.role)
                appendCharTo(new_html_list, exp_locs[2][1], exp_locs[3][0], html_temp)
                appendAfterGen(new_html_list, exp.descript)
                appendCharTo(new_html_list, exp_locs[3][1], exp_locs[0][1], html_temp)
            old_loc = exp_locs[0][1]
            exps = None

        if (capture == "educ_item" or "educ_" in capture):
            if capture == "educ_item":
                educs = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            educ_locs.append(loc)
            if not keys[-1] == capture:
                continue

        if educs:
            for educ in educs:
                appendCharTo(new_html_list, educ_locs[0][0], educ_locs[1][0], html_temp)
                appendAfterGen(new_html_list, f"{educ.start_date}--{educ.end_date}")
                appendCharTo(new_html_list, educ_locs[1][1], educ_locs[2][0], html_temp)
                appendAfterGen(new_html_list, educ.name)
                appendCharTo(new_html_list, educ_locs[2][1], educ_locs[3][0], html_temp)
                appendAfterGen(new_html_list, educ.descript)
                appendCharTo(new_html_list, educ_locs[3][1], educ_locs[0][1], html_temp)
            old_loc = educ_locs[0][1]
            educs = None

        if not keys[-1] == capture:
            appendCharTo(new_html_list, old_loc, loc[0], html_temp)
        else:
            appendCharTo(new_html_list, old_loc, len(html_temp), html_temp)

        if substit:
            appendAllSrcTo(new_html_list, substit)
        old_loc = loc[1]

    new_html = "".join(new_html_list)
    return new_html

def appendCharTo(char_list, from_i, to_i, source):
    for char in genHtmlFromUntil(from_i, to_i, source):
        char_list.append(char)

def appendAllSrcTo(char_list, gen_func):
    for char in gen_func:
        char_list.append(char)

def appendAfterGen(char_list, str_src):
    for char in genHtmlFromUntil(0, len(str_src), str_src):
        char_list.append(char)

def genHtmlFromUntil(from_i, to_i, source):
    while from_i < to_i:
        yield source[from_i]
        from_i += 1

def linkStyle(name):
    if name == "twitter":
        source = "fa-twitter"
    if name == "linkedin":
        source = "fa-linkedin"
    return genHtmlFromUntil(0, len(source), source)



def genRequiredFieldFrom(cv, prof, capture):
    if capture == "temp_name":
        return genHtmlFromUntil(0, len(cv.name), cv.name)

    if capture == "temp_css":
        return genHtmlFromUntil(0, len(cv.css), cv.css)

    if capture == "img":
        source = f'{prof.profile_pic}'
        return genHtmlFromUntil(0, len(source), source)

    if capture == "hum_name":
        source = f'{prof.user.first_name} {prof.user.last_name}'
        return genHtmlFromUntil(0, len(source), source)

    if capture == "prof_bullet":
        length = len(prof.bullet_descript)
        return genHtmlFromUntil(0, length, prof.bullet_descript)

    if capture == "prof_address":
        length = len(prof.address)
        return genHtmlFromUntil(0, length, prof.address)

    if capture == "prof_desc":
        length = len(prof.descript)
        return genHtmlFromUntil(0, length, prof.descript)

    if capture == "hum_bar":
        bar_val_list = prof.bar_set.all().values_list('decider', flat=True).distinct()
        bar_groupby = {}
        for val in bar_val_list:
            bar_groupby[val] = prof.bar_set.filter(decider=val)
        return bar_groupby

    if capture == "link_item":
        links = prof.links
        linkArr = links.splitlines()
        rg = r"[^~]+www.(.+).com[^~]+\/([^~]+)\/"
        linkHash = {}
        linkHash["name"] = []
        linkHash["id"] = []
        for link in linkArr:
            m = re.match(rg, link)
            linkHash["name"].append(m.group(1))
            linkHash["id"].append(m.group(2))
        return linkHash
    exp_val_list = prof.experience_set.all().values_list('decider', flat=True).distinct()
    exp_groupby = {}
    for val in exp_val_list:
        exp_groupby[val] = prof.experience_set.filter(decider=val)
    if capture == "exp_item":
        return exp_groupby['Exp']
    if capture == "educ_item":
        return exp_groupby['Ed']




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
        ] )
        all_formsets.append(exp_formset)

        ed_formset = forms.EducationFormSet( instance=profile, prefix='educations', initial= [
            { 'decider': 'Ed',}
        ] )
        all_formsets.append(ed_formset)

        lang_formset = forms.LangFormSet( instance=profile, prefix='languages', initial=[
            { 'decider': 'Lang', }
        ] )
        all_formsets.append(lang_formset)

        tech_formset = forms.TechFormSet( instance=profile, prefix='techs', initial=[
            { 'decider': 'Tech', }
        ] )
        all_formsets.append(tech_formset)

        skill_formset = forms.SkillFormSet( instance=profile, prefix='skills', initial=[
            { 'decider': 'Skill', }
        ] )
        all_formsets.append(skill_formset)

        award_formset = forms.AwardFormSet( instance=profile, prefix='awards', initial=[
            { 'decider': 'Award' }
        ] )
        all_formsets.append(award_formset)

        public_formset = forms.PublicFormSet( instance=profile, prefix="publications", initial=[
            { 'decider': 'Pub' }
        ] )
        all_formsets.append(public_formset)

        project_formset = forms.ProjectFormSet( instance=profile, prefix="projects" )
        all_formsets.append(project_formset)

    return all_formsets

def valid_for(formsets):
    for formset in formsets:
        for form in formset:
            if not form.is_valid():
                return False
    return True

def return_after_saving(formsets):
    for formset in formsets:
        formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        formset.save()


