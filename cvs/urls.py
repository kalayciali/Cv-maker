from django.urls import path

from . import views

urlpatterns = [
    path('', views.manage_cv, name='manage-cv'),
    path('index/', views.index_cvs, name='index-cvs')
]
