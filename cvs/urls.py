from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.manage_cv, name='manage-cv'),
    path('index/', views.index_cvs, name='index-cvs')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
