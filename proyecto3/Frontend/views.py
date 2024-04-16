from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt

def upload_to_flask(request):
    if request.method == 'POST':
        # Verificar si se envió un archivo
        if 'archivo' not in request.FILES:
            return HttpResponse('No se envió ningún archivo', status=400)

        archivo = request.FILES['archivo']

        # Verificar si se seleccionó un archivo
        if archivo.name == '':
            return HttpResponse('No se seleccionó ningún archivo', status=400)

        # Construir la URL del servidor Flask
        url_flask = 'http://localhost:4700/upload'

        # Enviar el archivo al servidor Flask
        files = {'archivo': archivo}
        response = requests.post(url_flask, files=files)

        # Verificar la respuesta del servidor Flask
        if response.status_code == 200:
            return HttpResponse('Archivo enviado correctamente a Flask', status=200)

        else:
            return HttpResponse('Error al enviar el archivo a Flask', status=500)

    else:
        # Si la solicitud no es POST, simplemente renderiza una página con el formulario de carga de archivos
        return render(request, 'Cargar_Config.html')

@csrf_exempt
def reset_to_flask(request):
    if request.method == 'POST':
        # Construir la URL del servidor Flask
        url_flask = 'http://localhost:4700/reset'

        response = requests.post(url_flask)

        # Verificar la respuesta del servidor Flask
        if response.status_code == 200:
            return HttpResponse('Base de datos Reseteada correctamente', status=200)

        else:
            return HttpResponse('Error resetear la base de datos', status=500)

    else:
        # Si la solicitud no es POST, simplemente renderiza una página con el formulario de carga de archivos
        return render(request, 'Resetear_datos.html')
    
# Create your views here.
def registrarCliente(request):
    return render(request, 'registrarCliente.html')
def Consultar_cuenta(request):
    return render(request, 'Consultar_cuenta.html')
def Resetear_datos(request):
    return render(request, 'Resetear_datos.html')
def Cargar_Config(request):
    return render(request, 'Cargar_Config.html')
def Cargar_Transac(request):
    return render(request, 'Cargar_Transac.html')
def Peticiones(request):
    return render(request, 'Peticiones.html')
def Ayuda(request):
    return render(request, 'Ayuda.html')
def Info_Estudiante(request):
    return render(request, 'Info_Estudiante.html')
def Info_pagina(request):
    return render(request, 'Info_pagina.html')
