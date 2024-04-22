from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as ET
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

def upload_transaccion_to_flask(request):
    if request.method == 'POST':
        # Verificar si se envió un archivo
        if 'archivo' not in request.FILES:
            return HttpResponse('No se envió ningún archivo', status=400)

        archivo = request.FILES['archivo']

        # Verificar si se seleccionó un archivo
        if archivo.name == '':
            return HttpResponse('No se seleccionó ningún archivo', status=400)

        # Construir la URL del servidor Flask
        url_flask = 'http://localhost:4700/uploadTransaccion'

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
        return render(request, 'Cargar_Transac.html')

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
def Consultar_Ingresos(request):
    return render(request, 'Consultar_Ingresos.html')
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
def tabla_clientes(request):
    # Leer el archivo XML de clientes
    tree_clientes = ET.parse('C:/Users/Player/Desktop/Carpeta GitHub Poryecto 3 IPC2/Guardado_Config.xml')
    root_clientes = tree_clientes.getroot()

    # Procesar los datos del archivo XML de clientes
    clientes = []
    for cliente_xml in root_clientes.findall('.//cliente'):
        nit = cliente_xml.find('NIT').text.strip()
        nombre = cliente_xml.find('nombre').text.strip()
        SaldoActual = cliente_xml.find('SaldoActual').text.strip()
        clientes.append({'nit': nit, 'nombre': nombre, 'SaldoActual': SaldoActual})

    # Leer el archivo XML de transacciones
    tree_transacciones = ET.parse('C:/Users/Player/Desktop/Carpeta GitHub Poryecto 3 IPC2/Guardado_Transaccion.xml')
    root_transacciones = tree_transacciones.getroot()

    # Procesar los datos del archivo XML de transacciones
    facturas = []
    for factura_xml in root_transacciones.findall('.//factura'):
        fecha = factura_xml.find('fecha').text.strip()
        valor = factura_xml.find('valor').text.strip()
        abono = factura_xml.find('Pago_Realizado').text.strip()
        facturas.append({'fecha': fecha, 'valor': valor, 'abono': abono})

    # Ordenar las facturas de la más reciente a la más antigua
    facturas = sorted(facturas, key=lambda x: x['fecha'], reverse=True)


    # Enumerar las facturas y los pagos para sincronizarlos
    enumeradas_facturas = list(enumerate(facturas))

    return render(request, 'Tabla_Clientes.html', {'clientes': clientes, 'enumeradas_facturas': enumeradas_facturas})

def Seleccionar_Cliente(request):
    return render(request, 'Consultar_Ingresos.html')
