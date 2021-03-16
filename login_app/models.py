from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re
import bcrypt

class UsuarioManager(models.Manager):
    def validador_registro(self, postData):
        error_reg = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            error_reg["email"] = "Ingresar email válido."

        if len(postData['nombre']) < 2:
            error_reg["nombre"] = "Ingresar nombre válido."
        if not str.isalpha(postData['nombre']):
            error_reg["nombre"] = "Ingresar nombre válido."
        if len(postData['apellido']) < 2:
            error_reg["apellido"] = "Ingresar apellido válido."
        if not str.isalpha(postData['apellido']):
            error_reg["apellido"] = "Ingresar apellido válido."

        if postData['cumple']:
            actual = date.today()
            nacimiento = date.fromisoformat(postData['cumple'])
            edad = actual.year - nacimiento.year
            if edad < 13:
                error_reg["cumple"] = "Solo puedes logearte si tienes 13 años o más."
        else:
            error_reg["cumple"] = "Debes ingresar tu fecha de nacimiento"

        if len(postData['password']) < 8:
            error_reg["password"] = "Ingresar password válido."
        if postData['password'] != postData['repassword']:
            error_reg['repassword'] = "Las password no coinciden."

        if postData['email']:
            if Usuario.objects.filter(cuenta__email__icontains=postData['email']):
                error_reg['email_usado'] = "El email ingresado ya se encuentra registrado."
        else:
            error_reg['email_usado'] = "Debes ingresar un email"
        return error_reg

    def validador_login(self, postData):
        error_log = {}
        try:
            user = Usuario.objects.get(cuenta__email=str(postData['login_email']))
            if bcrypt.checkpw(postData['login_password'].encode(), user.cuenta.password.encode()):
                return error_log
            else:
                error_log['password'] = "La contraseña ingresada no es valida"
                return error_log
        except:
            error_log['login_email'] = "El email ingresado no se encuentra registrado"
            return error_log

    def validador_password(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return hash1

class Cuenta(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cumple = models.DateField(max_length=20)
    cuenta = models.ForeignKey(Cuenta, related_name='usuario', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsuarioManager()
