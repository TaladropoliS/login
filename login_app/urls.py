from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('registro', views.registro),
    path('login', views.login),
    path('logout', views.logout)
    ]