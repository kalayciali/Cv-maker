from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    re_path(r'$', views.manage_cv, name='manage-cv'),
    re_path(r'index/$', views.index_cvs, name='index-cvs'),
    re_path(r'index/ajax/gen_img/$', views.generate_image, name='gen-img'),
    re_path(r'show/(?P<idx>\d+)/$', views.show_cv, name='show-cv')
]
