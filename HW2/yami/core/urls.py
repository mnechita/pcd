from django.conf.urls import url
from django.views.generic import TemplateView

from core import views as views
from django.urls import path

urlpatterns = [
    url(r'accounts/signup', views.signup, name='signup'),
    url(r'accounts/login', views.login, name='login'),
    url(r'/', views.home, name='home'),
    url(r'upload', views.upload, name='upload'),
]
