from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from accounts.models import Profile
from django.http import HttpResponse, FileResponse, JsonResponse
from django.template.loader import render_to_string
import json
import re
import os
from django.conf import settings
from collections import OrderedDict
from weasyprint import HTML


# Create your views here.

@login_required
def manage_cv(request):
    profile = request.user.profile
    if request.method == "POST":
        all_formsets = generate_formsets(request, profile)
        with transaction.atomic():
            if valid_for(all_formsets):
                for formset in all_formsets:
                    formset.save()
                return redirect('index-cvs')
            else:
                errs = []
                for formset in all_formsets:
                    errs.append(formset.errors)
                return render(request, 'cvs/manage_cv.html', {
                    'errs': errs,
                    'all_formsets': all_formsets
                })
    else:
        exp_queryset = models.Experience.objects.filter(decider='Exp')
        first_formset = forms.ExperienceFormSet( instance=profile, prefix='experiences', initial= [
            {'decider': 'Exp',}
        ], queryset = exp_queryset )
        return render(request, 'cvs/manage_cv.html', {
            'formset': first_formset
        })

def generate_form(request):
    # ajax call
    form_title = request.GET.get('title', None)
    profile = request.user.profile
    lang_queryset = models.Bar.objects.filter(decider='Lang')
    tech_queryset = models.Bar.objects.filter(decider='Tech')
    skill_queryset = models.Bar.objects.filter(decider='Skill')
    educ_queryset = models.Experience.objects.filter(decider='Ed')
    award_queryset = models.Award.objects.filter(decider='Award')
    public_queryset = models.Award.objects.filter(decider='Pub')

    if form_title == "Eğitimler":
        formset = forms.EducationFormSet( instance=profile, prefix='educations', initial= [
            { 'decider': 'Ed',}
        ], queryset= educ_queryset )
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset, 'title': form_title })

    if form_title == "Projeler":
        formset = forms.ProjectFormSet( instance=profile, prefix="projects")
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset , 'title': form_title})

    if form_title == "Diller":
        formset = forms.LangFormSet( instance=profile, prefix='languages', initial=[
            { 'decider': 'Lang', }
        ] , queryset = lang_queryset)
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset , 'title': form_title})

    if form_title == "Teknoloji":
        formset = forms.TechFormSet( instance=profile, prefix='techs', initial=[
            { 'decider': 'Tech', }
        ], queryset = tech_queryset)
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset, 'title': form_title })

    if form_title == "Yetenekler":
        formset = forms.SkillFormSet( instance=profile, prefix='skills', initial=[ {'decider': 'Skill', } ], queryset = skill_queryset )
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset, 'title': form_title })

    if form_title == "Ödüller":
        formset = forms.AwardFormSet( instance=profile, prefix='awards', initial=[
            { 'decider': 'Award' }
        ], queryset = award_queryset )
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset , 'title': form_title})

    if form_title == "Yayın-Sertifika":
        formset = forms.PublicFormSet( instance=profile, prefix="publications", initial=[
            { 'decider': 'Pub' }
        ], queryset = public_queryset )
        form_as_str = render_to_string('cvs/form.html', { 'formset': formset, 'title': form_title })

    data = { 'form_html': form_as_str }
    return JsonResponse(data)


@login_required
def index_cvs(request):
    profile = request.user.profile
    first_cv = models.Cv.objects.get(id=18)
    newHtml = generateHtml(first_cv.loc_data, first_cv, profile)
    html = HTML(string=newHtml, base_url=request.build_absolute_uri("/"))
    file = open(os.path.join(settings.BASE_DIR,  f'cvs/static/cvs/{request.user.username}{first_cv.id}.png'), 'wb+')
    html.write_png(target=file, resolution=40)
    return render(request, 'cvs/index_cvs.html', { 'first_url': f"cvs/{request.user.username}{first_cv.id}.png", })

def generate_image(request):
    # ajax call
    idx = request.GET.get('idx', None)
    try:
        cv = models.Cv.objects.get(pk=idx)
        profile = request.user.profile
        next_html = generateHtml(cv.loc_data, cv, profile)
        html = HTML(string=next_html, base_url=request.build_absolute_uri('/'))
        file = open(os.path.join(settings.BASE_DIR,  f'cvs/static/cvs/{request.user.username}{idx}.png'), 'wb+')
        html.write_png(target=file, resolution=40)
        next_url = os.path.join(settings.BASE_DIR,  f'cvs/static/cvs/{request.user.username}{idx}.png')
    except models.Cv.DoesNotExist:
        next_url = None

    data = {
        'img_url': next_url,
    }
    return JsonResponse(data)

@login_required
def info_cv(request):
    user = request.user
    profile_id = request.user.profile.id
    lang_queryset = models.Bar.objects.filter(decider='Lang')
    tech_queryset = models.Bar.objects.filter(decider='Tech')
    skill_queryset = models.Bar.objects.filter(decider='Skill')
    exp_queryset = models.Experience.objects.filter(decider='Exp')
    educ_queryset = models.Experience.objects.filter(decider='Ed')
    award_queryset = models.Award.objects.filter(decider='Award')
    public_queryset = models.Award.objects.filter(decider='Pub')
    prof_with_all_fields = Profile.objects.filter(id=profile_id).prefetch_related(
        Prefetch("experience_set", queryset=exp_queryset, to_attr='prefetched_exps'),
        Prefetch("experience_set", queryset=educ_queryset, to_attr='prefetched_educs'),
        Prefetch("bar_set", queryset=lang_queryset, to_attr='prefetched_langs'),
        Prefetch("bar_set", queryset=tech_queryset, to_attr='prefetched_techs'),
        Prefetch("bar_set", queryset=skill_queryset, to_attr='prefetched_skills'),
        Prefetch("award_set", queryset=award_queryset, to_attr='prefetched_awards'),
        Prefetch("award_set", queryset=public_queryset, to_attr='prefetched_publics'),
        Prefetch("project_set", to_attr='prefetched_projects')
    )
    return render(request, 'cvs/info_cv.html', {
        'user': user,
        'prof_with_all_fields': prof_with_all_fields
        })

@login_required
def show_cv(request, idx):
    cv = models.Cv.objects.get(id=idx)
    profile = request.user.profile
    new_html = generateHtml(cv.loc_data, cv, profile)
    html = HTML(string=new_html, base_url=request.build_absolute_uri('/'))
    result = html.write_pdf()

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'filename={cv.name}.pdf'
    prof_cv = models.ProfileCv(profile=profile, cv=cv, new_html=new_html)
    prof_cv.save()
    return response



# Helper functions

def valid_for(formsets):
    for formset in formsets:
        for form in formset:
            if not form.is_valid():
                return False
    return True

def generate_formsets(request, profile):
    # generate formsets for post
    all_formsets = []
    exp_formset = forms.ExperienceFormSet(request.POST, instance=profile, prefix='experiences')
    all_formsets.append(exp_formset)

    ed_formset = forms.EducationFormSet(request.POST, initial= [ { 'decider': 'Ed',} ],  
                                        instance=profile, prefix='educations')
    all_formsets.append(ed_formset)

    lang_formset = forms.LangFormSet(request.POST, initial=[ { 'decider': 'Lang', } ] , 
                                     instance=profile, prefix='languages')
    all_formsets.append(lang_formset)

    tech_formset = forms.TechFormSet(request.POST, initial=[ { 'decider': 'Tech', } ], 
                                     instance=profile, prefix='techs')
    all_formsets.append(tech_formset)

    skill_formset = forms.SkillFormSet(request.POST, initial=[ {'decider': 'Skill', } ], instance=profile, prefix='skills')
    all_formsets.append(skill_formset)

    award_formset = forms.AwardFormSet(request.POST, initial=[ { 'decider': 'Award' } ], 
                                       instance=profile, prefix='awards')
    all_formsets.append(award_formset)

    public_formset = forms.PublicFormSet(request.POST, initial=[ { 'decider': 'Pub' } ], 
                                         instance=profile, prefix="publications")
    all_formsets.append(public_formset)

    project_formset = forms.ProjectFormSet(request.POST, instance=profile, prefix="projects")
    all_formsets.append(project_formset)

    return all_formsets

# HTML generation functions

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


def generateHtml(locData, cv, prof):
    loc_data = json.loads(locData, object_pairs_hook=OrderedDict)
    # locations as list [[start_idx, end_idx], ..]
    # loc_data arranged in such a way that it has unimportant loc item between 
    # multiple number items such as experience, educ, award in order to follow the order of them

    html_temp = cv.html
    new_html_list = []
    old_loc = 0

    bar_locs = []
    link_locs = []
    exp_locs = []
    educ_locs = []
    project_locs = []
    award_locs = []

    bars = None
    links = None
    exps = None
    educs = None
    projects = None
    awards = None


    for capture in loc_data:

        substit = genRequiredFieldFrom(cv, prof, capture)
        loc = loc_data[capture]

        if (capture == "hum_bar" or "bar_" in capture ):
            if capture == "hum_bar":
                bars = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            if capture == "bar_style_without_num":
                otherStyle = True

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
                    if len(bar_locs) > 5:
                        appendAfterGen(new_html_list, bar.name)
                        appendCharTo(new_html_list, bar_locs[3][1], bar_locs[4][0], html_temp)
                        appendAfterGen(new_html_list, f"width: {bar.star}%;")
                        appendCharTo(new_html_list, bar_locs[4][1], bar_locs[5][0], html_temp)
                        appendAfterGen(new_html_list, f"{bar.star}%")
                        appendCharTo(new_html_list, bar_locs[5][1], bar_locs[2][1], html_temp)
                    else:
                        if otherStyle:
                            appendAfterGen(new_html_list, bar.name)
                            appendCharTo(new_html_list, bar_locs[3][1], bar_locs[4][0], html_temp)
                            appendAfterGen(new_html_list, f"width: {bar.star}%;")
                            appendCharTo(new_html_list, bar_locs[4][1], bar_locs[2][1], html_temp)
                        else:
                            appendAllSrcTo(new_html_list,barStyle(title))
                            appendCharTo(new_html_list, bar_locs[3][1], bar_locs[4][0], html_temp)
                            appendAfterGen(new_html_list, bar.name)
                            appendCharTo(new_html_list, bar_locs[4][1], bar_locs[2][1], html_temp)

                appendCharTo(new_html_list, bar_locs[2][1], bar_locs[0][1], html_temp)
            old_loc = bar_locs[0][1]
            bars = None

        if (capture == "link_item" or "link_" in capture):
            if capture == "link_item":
                links = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            link_locs.append(loc)
            # continue until links finished
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
            # continue until exps finished
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
            # continue until educs finished
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

        if (capture == "project_item" or "project_" in capture):
            if capture == "project_item":
                projects = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            project_locs.append(loc)
            # continue until projects finished
            continue

        if projects:
            for project in projects:
                appendCharTo(new_html_list, project_locs[0][0], project_locs[1][0], html_temp)
                appendAfterGen(new_html_list, project.name )
                appendCharTo(new_html_list, project_locs[1][1], project_locs[2][0], html_temp)
                appendAfterGen(new_html_list, project.role)
                appendCharTo(new_html_list, project_locs[2][1], project_locs[3][0], html_temp)
                appendAfterGen(new_html_list, project.descript)
                appendCharTo(new_html_list, project_locs[3][1], project_locs[0][1], html_temp)
            old_loc = project_locs[0][1]
            projects = None

        if (capture == "award_item" or "award_" in capture):
            if capture == "award_item":
                awards = substit
                appendCharTo(new_html_list, old_loc, loc[0], html_temp)
            award_locs.append(loc)
            # continue until awards finished
            continue

        if awards:
            for award in awards:
                appendCharTo(new_html_list, award_locs[0][0], award_locs[1][0], html_temp)
                appendAfterGen(new_html_list, award.name )
                appendCharTo(new_html_list, award_locs[1][1], award_locs[2][0], html_temp)
                appendAfterGen(new_html_list, award.date.strftime("%Y"))
                appendCharTo(new_html_list, award_locs[2][1], award_locs[0][1], html_temp)
            old_loc = award_locs[0][1]
            awards = None

        # before substitution
        appendCharTo(new_html_list, old_loc, loc[0], html_temp)

        # substitution
        if substit:
            appendAllSrcTo(new_html_list, substit)
        else:
            appendCharTo(new_html_list, loc[0], loc[1], html_temp)

        # move cursor after substitution
        old_loc = loc[1]


    new_html = "".join(new_html_list)
    return new_html


def linkStyle(name):
    if name == "twitter":
        source = "fa-twitter"
    if name == "linkedin":
        source = "fa-linkedin"
    return genHtmlFromUntil(0, len(source), source)

def barStyle(name):
    if name == "Skill":
        source = "fas fa-check-double"
    elif name == "Tech":
        source = "fab fa-linux"
    else:
        source = "fas fa-globe"
    return genHtmlFromUntil(0, len(source), source)


def genRequiredFieldFrom(cv, prof, capture):
    # it generates required fields 

    if capture == "temp_name":
        return genHtmlFromUntil(0, len(cv.name), cv.name)

    if capture == "temp_css":
        return genHtmlFromUntil(0, len(cv.css), cv.css)

    if capture == "img":
        source = f'media/{prof.profile_pic.name}'
        return genHtmlFromUntil(0, len(source), source)

    if capture == "hum_name":
        source = f'{prof.user.first_name} {prof.user.last_name}'
        return genHtmlFromUntil(0, len(source), source)
    if capture == "hum_mail":
        source = f'{prof.user.email}'
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
    
    if capture == "project_item":
        project_all = prof.project_set.all()
        return project_all

    if capture == "award_item":
        award_all = prof.award_set.all()
        return award_all

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




