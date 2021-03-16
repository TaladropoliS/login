from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Usuario, Cuenta
from django.db.models import Q, Max, Count, F
# Create your views here.

def inicio(request):
    request.session['log_user'] = 0
    return render(request, 'login.html')


def login(request):
    if request.method == "POST":
        error_log = Usuario.objects.validador_login(request.POST)
        if len(error_log) > 0:
            print('error en el login')
        else:
            request.session['log_user'] = request.POST['login_email']
        return redirect('/exito')
    return redirect('/')

def logeado(request):
    if request.session['log_user']!=0:
        usuario = Usuario.objects.all()
        context = {

        }
        return render(request, "logeado.html", context)
    else:
        return redirect('/')


def registro(request):
    if request.method == "POST":
        error_reg = Usuario.objects.validador_usuario(request.POST)
        password = Usuario.objects.password_hash(request.POST)
        if len(error_reg) > 0:
            for key, value in error_reg.items():
                messages.error(request, value)
            return redirect('/')
        else:
            usuario_ = Cuenta.objects.create(email=request.POST['email'],
                                  password=password)
            Usuario.objects.create(nombre=request.POST['nombre'],
                                   apellido=request.POST['apellido'],
                                   cumple=request.POST['cumple'],
                                   cuenta=usuario_)
            return redirect('/registrado')
    return redirect('/')

def registrado(request):
    return render(request, 'logeado.html')


def logout(request):
    request.session['log_user'] = 0
    return redirect('/')