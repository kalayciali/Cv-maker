from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'show/(?P<idx>\d+)/$', views.show_cv, name='show-cv'),
    url(r'inform/$', views.info_cv, name='info-cv'),
    url(r'index/$', views.index_cvs, name='index-cvs'),
    url(r'index/ajax/gen_img/$', views.generate_image, name='gen-img'),
    url(r'manage/$', views.manage_cv, name='manage-cv'),
    url(r'manage/ajax/gen_form/$', views.generate_form, name='gen-form'),
]
