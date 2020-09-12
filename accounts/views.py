from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Profile

def index(request):
    return render(request, 'accounts/home.html')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:index'))

def sign_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.bullet_descript= form.cleaned_data.get('bullet_descript')
            user.profile.descript= form.cleaned_data.get('descript')
            user.profile.phone_num= form.cleaned_data.get('phone_num')
            user.profile.address= form.cleaned_data.get('address')
            user.profile.links= form.cleaned_data.get('links')
            user.profile.profile_pic = request.FILES['profile_pic']
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts:index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', { 'form': form })

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return HttpResponseRedirect(reverse('accounts:index'))
        else:
            err = "Kullanıcı adı ve şifre birbiriyle uyuşmuyor."
            return render(request, 'accounts/login.html', { 'err': err })
    else:
        return render(request, 'accounts/login.html', {})
