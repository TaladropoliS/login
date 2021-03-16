from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Usuario, Cuenta
from django.db.models import Q, Max, Count, F
# Create your views here.

def inicio(request):
    request.session['log_name'] = ""
    request.session['log_email'] = ""
    request.session['log_user'] = 0
    return render(request, 'login.html')


def login(request):
    if request.method == "POST":
        error_log = Usuario.objects.validador_login(request.POST)
        if len(error_log) > 0:
            request.session['mensaje'] = 1
            for key, value in error_log.items():
                request.session['error_login'] = messages.error(request, value)
                print(key, value)
            return redirect('/')
        else:
            request.session['log_user'] = request.POST['login_email']
            users = Usuario.objects.get(cuenta__email__icontains=request.POST['login_email'])
            request.session['log_name'] = f"{users.nombre} {users.apellido}"
            request.session['log_email'] = f"{users.cuenta.email}"
            request.session['log_id'] = f"{users.cuenta.id}"
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
        error_reg = Usuario.objects.validador_registro(request.POST)
        if len(error_reg) > 0:
            request.session['mensaje'] = 0
            for key, value in error_reg.items():
                request.session['error_registro'] = messages.error(request, value)
            return redirect('/')
        else:
            password = Usuario.objects.validador_password(request.POST)
            usuario_t = Cuenta.objects.create(email=request.POST['email'],
                                  password=password)
            Usuario.objects.create(nombre=request.POST['nombre'],
                                   apellido=request.POST['apellido'],
                                   cumple=request.POST['cumple'],
                                   cuenta=usuario_t)
            return redirect('/registrado')
    return redirect('/')

def registrado(request):
    return render(request, 'logeado.html')


def logout(request):
    request.session['log_name'] = ""
    request.session['log_email'] = ""
    request.session['log_user'] = 0
    return redirect('/')