from email import message
from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
from gestionPedidos.models import Articulos
from django.core.mail import send_mail
from django.conf import settings
from gestionPedidos.forms import FormularioContacto

# Create your views here.

def busqueda_productos(request):
    return render(request, 'busqueda_productos.html')

def buscar(request):
    if request.GET['prd']:
        # mensaje = 'Articulo buscado: %r' %request.GET['prd']
        producto = request.GET['prd']
        if len(producto) > 20:  # Control de rango del nombre buscado
            mensaje = "Fuera de rango"
        else:
            articulos = Articulos.objects.filter(nombre__icontains = producto)
            return render(request, 'resultados_busqueda.html', {'articulos': articulos, 'query': producto})
    else:
        mensaje = 'Busqueda en blanco'
    return HttpResponse(mensaje)

"""
FORMA SIMPLE

def contacto(request):
    if request.method == 'POST':
        subject = request.POST['asunto']
        message = request.POST['mensaje'] + "" + request.POST['email']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['curso@gmail.com']
        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'gracias.html')
    
    return render(request, 'contacto.html')
"""

def contacto(request): # FORMA CON FORMS
    if request.method == 'POST':
        miFormulario = FormularioContacto(request.POST)
        if miFormulario.is_valid():
            infForm = miFormulario.changed_data
            send_mail(infForm['asunto'], infForm['mensaje'],
            infForm.get('email', ''), ['a@gmail.com'], )
        return render(render, 'gracias.html')
    else:
        miFormulario = FormularioContacto()
    return render(request, 'formulario_contacto.html', {'form':miFormulario})