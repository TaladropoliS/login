from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Usuario, Cuenta
from django.db.models import Q, Max, Count, F
# Create your views here.

def inicio(request):
    return render(request, 'login.html')