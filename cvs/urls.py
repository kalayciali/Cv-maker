from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.manage_cv, name='manage-cv'),
    path('index/', views.index_cvs, name='index-cvs'),
    url(r'^index/ajax/gen_img/$', views.generate_image, name='gen-img')
]
