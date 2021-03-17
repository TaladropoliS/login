from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Usuario, Cuenta
from datetime import date
from django.contrib.auth import logout as do_logout
from django.db.models import Q, Max, Count, F
# Create your views here.

def inicio(request):
    request.session['log_name'] = ""
    request.session['log_email'] = ""
    request.session['log_id'] = ""
    request.session['log_edad'] = 0
    request.session['log_user'] = 0
    return render(request, 'login.html')


def login(request):
    if request.method == "POST":
        error_log = Usuario.objects.validador_login(request.POST)
        if len(error_log) > 0:
            request.session['mensaje'] = 1
            for key, value in error_log.items():
                request.session['error_log'] = messages.error(request, value)
            return redirect('/')
        else:
            request.session['log_user'] = request.POST['login_email']
            users = Usuario.objects.get(cuenta__email__icontains=request.POST['login_email'])
            request.session['log_name'] = f"{users.nombre} {users.apellido}"
            request.session['log_email'] = f"{users.cuenta.email}"
            request.session['log_id'] = f"{users.cuenta.id}"
            actual = date.today()
            nacimiento = users.cumple
            edad = actual.year - nacimiento.year
            request.session['log_edad'] = f"{edad}"
        return render(request, "logeado.html")
    return redirect('/')

def registro(request):
    if request.method == "POST":
        error_reg = Usuario.objects.validador_registro(request.POST)
        if len(error_reg) > 0:
            request.session['mensaje'] = 0
            for key, value in error_reg.items():
                request.session['error_reg'] = messages.error(request, value)
            return redirect('/')
        else:
            password = Usuario.objects.validador_password(request.POST)
            usuario_t = Cuenta.objects.create(email=request.POST['email'],
                                  password=password)
            Usuario.objects.create(nombre=request.POST['nombre'],
                                   apellido=request.POST['apellido'],
                                   cumple=request.POST['cumple'],
                                   cuenta=usuario_t)
            # AUTO LOGIN #
            request.session['log_user'] = request.POST['email']
            users = Usuario.objects.get(cuenta__email__icontains=request.POST['email'])
            request.session['log_name'] = f"{users.nombre} {users.apellido}"
            request.session['log_email'] = f"{users.cuenta.email}"
            request.session['log_id'] = f"{users.cuenta.id}"
            actual = date.today()
            nacimiento = users.cumple
            edad = actual.year - nacimiento.year
            request.session['log_edad'] = f"{edad}"
        return render(request, "logeado.html")
            # FIN AUTO LOGIN #
    return redirect('/')

def logout(request):
    request.session['log_user'] = ""
    request.session['log_name'] = ""
    request.session['log_email'] = ""
    request.session['log_id'] = ""
    request.session['log_edad'] = 0
    request.session['registrado'] = 0
    do_logout(request)
    return redirect('/login')