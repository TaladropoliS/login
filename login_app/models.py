from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UsuarioManager(models.Manager):
    def validador_usuario(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Ingresar EMAIL válido."

        if len(postData['nombre']) < 2:
            errors["nombre"] = "Ingresar NOMBRE válido."
        if not str.isalpha(postData['nombre']):
            errors["nombre"] = "Ingresar NOMBRE válido."
        if len(postData['apellido']) < 2:
            errors["apellido"] = "Ingresar APELLIDO válido."
        if not str.isalpha(postData['apellido']):
            errors["apellido"] = "Ingresar APELLIDO válido."
        if len(postData['cumple']) < 13:
            errors["cumple"] = "Solo puedes logearte si tienes 13 años o más."
        if len(postData['password']) < 8:
            errors["password"] = "Ingresar PASSWORD válido."
        if postData['password'] != postData['repassword']:
            error['repassword'] = "Las PASSWORD no coinciden."
        if Usuario.objects.filter(cuenta__email__icontains=postData['email']):
            error['email_usado'] = "El email ingresado ya se encuentra registrado."
        return errors

    def validador_login(self, postData):
        error = {}
        user = Usuario.objects.get(cuenta__email=str(postData['login_email']))
        if user:
            if bcrypt.checkpw(postData['login_password'].encode(), user.cuenta.password.encode()):
                return error
            else:
                error['password-revision'] = "La contraseña ingresada no es valida"
        else:
            error['login_email'] = f"{postData['login_email']} no se encuentra registrado"
        return error

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
