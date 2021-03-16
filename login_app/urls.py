from django.urls import path
from . import views
urlpatterns = [
    path('', views.inicio),

    path('registro', views.registro),
    path('registrado', views.registrado),

    path('login', views.login),
    path('exito', views.logeado),

    path('logout', views.logout)
    ]