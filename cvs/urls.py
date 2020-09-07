from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_cv, name='manage-cv')
]
