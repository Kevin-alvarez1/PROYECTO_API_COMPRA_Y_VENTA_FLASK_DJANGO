from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta

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
def Consultar_ingresos(request):    
    return render(request, 'Consultar_ingresos.html')
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
        SaldoActual = factura_xml.find('SaldoActual').text.strip()
        facturas.append({'fecha': fecha, 'valor': valor, 'abono': abono, 'SaldoActual': SaldoActual})

        # Actualizar el saldo actual del cliente correspondiente en la lista de clientes
        for cliente in clientes:
            if cliente['nit'] == factura_xml.find('NITcliente').text.strip():
                cliente['SaldoActual'] = SaldoActual
                break

    # Ordenar las facturas de la más reciente a la más antigua
    facturas = sorted(facturas, key=lambda x: x['fecha'], reverse=True)

    # Enumerar las facturas y los pagos para sincronizarlos
    enumeradas_facturas = list(enumerate(facturas))

    return render(request, 'Tabla_Clientes.html', {'clientes': clientes, 'enumeradas_facturas': enumeradas_facturas})



def Seleccionar_cliente(request):
    if request.method == 'POST':
        nit = request.POST.get('Nit')
     # Leer el archivo XML de clientes
        tree_clientes = ET.parse('C:/Users/Player/Desktop/Carpeta GitHub Poryecto 3 IPC2/Guardado_Config.xml')
        root_clientes = tree_clientes.getroot()
        clientes = []
        for cliente_xml in root_clientes.findall('.//cliente'):
            if cliente_xml.find('NIT').text.strip() == nit:
                nombre = cliente_xml.find('nombre').text.strip()
                saldo_actual = cliente_xml.find('SaldoActual').text.strip()
                clientes.append({'nit': nit, 'nombre': nombre, 'saldo_actual': saldo_actual})
   
        # Procesar los datos del archivo XML de clientes
        cliente_encontrado = None
        for cliente_xml in root_clientes.findall('.//cliente'):
            if cliente_xml.find('NIT').text.strip() == nit:
                nombre = cliente_xml.find('nombre').text.strip()
                saldo_actual = cliente_xml.find('SaldoActual').text.strip()
                cliente_encontrado = {'nit': nit, 'nombre': nombre, 'saldo_actual': saldo_actual}
                break

        if cliente_encontrado is not None:
            # Leer el archivo XML de transacciones
            tree_transacciones = ET.parse('C:/Users/Player/Desktop/Carpeta GitHub Poryecto 3 IPC2/Guardado_Transaccion.xml')
            root_transacciones = tree_transacciones.getroot()

            # Procesar los datos del archivo XML de transacciones
            facturas = []
            for factura_xml in root_transacciones.findall('.//factura'):
                if factura_xml.find('NITcliente').text.strip() == nit:
                    fecha = factura_xml.find('fecha').text.strip()
                    valor = factura_xml.find('valor').text.strip()
                    abono = factura_xml.find('Pago_Realizado').text.strip()
                    saldo_actual = factura_xml.find('SaldoActual').text.strip()
                    facturas.append({'fecha': fecha, 'valor': valor, 'abono': abono, 'SaldoActual': saldo_actual})
                # Actualizar el saldo actual del cliente correspondiente en la lista de clientes
                for cliente in clientes:
                    if cliente['nit'] == factura_xml.find('NITcliente').text.strip():
                        cliente['SaldoActual'] = saldo_actual
                        break

            # Ordenar las facturas de la más reciente a la más antigua
            facturas = sorted(facturas, key=lambda x: x['fecha'], reverse=True)

            # Enumerar las facturas y los pagos para sincronizarlos
            enumeradas_facturas = list(enumerate(facturas))

            return render(request, 'cliente_encontrado.html', {'cliente': clientes, 'enumeradas_facturas': enumeradas_facturas})
        else:
            # Cliente no encontrado
            return render(request, 'Seleccionar_cliente.html', {'error_message': 'Cliente no encontrado', 'nit': nit})
    else:
        # Si la solicitud es GET, simplemente renderiza la página
        return render(request, 'Seleccionar_cliente.html')

def Consultar_ingresos_Mes(request):
    if request.method == 'POST':
        mes = request.POST.get('mes')
        try:
            # Convertir el mes ingresado a un objeto datetime para comparación
            fecha_seleccionada = datetime.strptime(mes, '%m/%Y')
            # Leer el archivo XML de transacciones
            tree_transacciones = ET.parse('C:/Users/Player/Desktop/Carpeta GitHub Poryecto 3 IPC2/Guardado_Transaccion.xml')
            root_transacciones = tree_transacciones.getroot()

            # Procesar los datos del archivo XML de transacciones
            pagos = []
            for pago_xml in root_transacciones.findall('.//pago'):
                fecha_pago_str = pago_xml.find('fecha').text.strip()
                fecha_pago = datetime.strptime(fecha_pago_str, '%d/%m/%Y')
                # Verificar si el pago está dentro del rango de meses seleccionados
                if fecha_pago.year == fecha_seleccionada.year and fecha_pago.month == fecha_seleccionada.month:
                    codigo_banco = pago_xml.find('codigoBanco').text.strip()
                    fecha = fecha_pago.strftime('%d/%m/%Y')  # Convertir la fecha al formato dd/MM/yyyy
                    valor = pago_xml.find('valor').text.strip()
                    pagos.append({'codigo_banco': codigo_banco, 'fecha': fecha, 'valor': valor})

            # Ordenar los pagos de la más reciente a la más antigua
            pagos = sorted(pagos, key=lambda x: x['fecha'], reverse=True)

            return render(request, 'Grafica_Ingresos.html', {'pagos': pagos})
        except ValueError:
            # Si el formato del mes ingresado no es válido
            return render(request, 'Consultar_ingresos.html', {'error_message': 'Formato de mes inválido. Ingrese el mes en el formato dd/MM/yyyy.'})
    else:
        # Si la solicitud es GET, simplemente renderiza la página
        return render(request, 'Consultar_ingresos.html')