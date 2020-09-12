from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.sign_user, name="sign-up"),
    path('accounts/login/', views.login_user, name="login-user"),
    path('accounts/logout/', views.logout_user, name="logout-user")
]
