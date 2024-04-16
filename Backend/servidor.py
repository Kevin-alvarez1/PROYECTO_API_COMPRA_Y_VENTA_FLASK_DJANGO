from flask import Flask, request
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re

app = Flask(__name__)

class RespuestaConfig:
    def __init__(self, clientes_creados, bancos_creados, clientes_actualizados, bancos_actualizados):
        self.clientes_creados = clientes_creados
        self.bancos_creados = bancos_creados
        self.clientes_actualizados = clientes_actualizados
        self.bancos_actualizados = bancos_actualizados

class RespuestaTranascion:
    def __init__(self, facturas_creadas, facturas_duplicadas, facturas_error, pagos_creados, pagos_duplicados, pagos_error):
        self.facturas_creadas = facturas_creadas
        self.facturas_duplicadas = facturas_duplicadas
        self.facturas_error = facturas_error
        self.pagos_creados = pagos_creados
        self.pagos_duplicados = pagos_duplicados
        self.pagos_error = pagos_error

def guardar_respuesta_transaccion(respuesta):
    root = ET.Element('respuesta')

    if respuesta.facturas_creadas is not None or respuesta.facturas_duplicadas is not None or respuesta.facturas_error is not None:
        facturas_element = ET.SubElement(root, 'facturas')
        if respuesta.facturas_creadas is not None:
            ET.SubElement(facturas_element, 'creadas').text = str(respuesta.facturas_creadas)
        if respuesta.facturas_duplicadas is not None:
            ET.SubElement(facturas_element, 'duplicadas').text = str(respuesta.facturas_duplicadas)
        if respuesta.facturas_error is not None:
            ET.SubElement(facturas_element, 'error').text = str(respuesta.facturas_error)

    if respuesta.pagos_creados is not None or respuesta.pagos_duplicados is not None or respuesta.pagos_error is not None:
        pagos_element = ET.SubElement(root, 'pagos')
        if respuesta.pagos_creados is not None:
            ET.SubElement(pagos_element, 'creados').text = str(respuesta.pagos_creados)
        if respuesta.pagos_duplicados is not None:
            ET.SubElement(pagos_element, 'duplicados').text = str(respuesta.pagos_duplicados)
        if respuesta.pagos_error is not None:
            ET.SubElement(pagos_element, 'error').text = str(respuesta.pagos_error)

    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    formatted_xml = remove_whitespace(xml_str)

    with open('respuesta_transaccion.xml', 'w') as file:
        file.write(formatted_xml)

def guardar_respuesta_config(respuesta):
    root = ET.Element('respuesta')

    if respuesta.clientes_creados is not None or respuesta.clientes_actualizados is not None:
        clientes_element = ET.SubElement(root, 'clientes')
        if respuesta.clientes_creados is not None:
            ET.SubElement(clientes_element, 'creados').text = str(respuesta.clientes_creados)
        if respuesta.clientes_actualizados is not None:
            ET.SubElement(clientes_element, 'actualizados').text = str(respuesta.clientes_actualizados)

    if respuesta.bancos_creados is not None or respuesta.bancos_actualizados is not None:
        bancos_element = ET.SubElement(root, 'bancos')
        if respuesta.bancos_creados is not None:
            ET.SubElement(bancos_element, 'creados').text = str(respuesta.bancos_creados)
        if respuesta.bancos_actualizados is not None:
            ET.SubElement(bancos_element, 'actualizados').text = str(respuesta.bancos_actualizados)

    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    formatted_xml = remove_whitespace(xml_str)

    with open('respuesta_config.xml', 'w') as file:
        file.write(formatted_xml)


def remove_whitespace(xml_string):
    lines = xml_string.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return "\n".join(non_empty_lines)

class Cliente:
    def __init__(self, Nit_Cliente, Nombre_Cliente):
        self.Nit_Cliente = Nit_Cliente
        self.Nombre_Cliente = Nombre_Cliente

class Banco:
    def __init__(self, Nombre_Banco, Codigo_Banco):
        self.Nombre_Banco = Nombre_Banco
        self.Codigo_Banco = Codigo_Banco

class Factura:
    def __init__(self, Numero_Factura, Nit_CLiente,Fecha_Factura,Valor_Factura):
        self.Numero_Factura = Numero_Factura
        self.Nit_Cliente = Nit_CLiente
        self.Fecha_Factura = Fecha_Factura
        self.Valor_Factura = Valor_Factura

class Pago:
    def __init__(self, Codigo_Banco, Fecha_Pago, Nit_Cliente, Valor_Pago):
        self.Codigo_Banco = Codigo_Banco
        self.Fecha_Pago = Fecha_Pago
        self.Nit_Cliente = Nit_Cliente
        self.Valor_Pago = Valor_Pago

def validar_nit(nit):
    # Patrón para NIT #######-#
    patron_nit = r'^\d{7}-\w$'
    
    # Verificar si el NIT coincide con el patrón
    if re.match(patron_nit, nit):
        return True
    else:
        return False

def actualizar_base_datos(archivo_guardado, nuevo_contenido):
    clientes = []
    bancos = []

    if os.path.exists(archivo_guardado):
        tree = ET.parse(archivo_guardado)
        root = tree.getroot()

        for cliente_xml in root.findall('.//cliente'):
            nit = cliente_xml.find('NIT').text.strip()
            nombre = cliente_xml.find('nombre').text.strip()
            clientes.append(Cliente(nit, nombre))

        for banco_xml in root.findall('.//banco'):
            codigo = banco_xml.find('codigo').text.strip()
            nombre = banco_xml.find('nombre').text.strip()
            bancos.append(Banco(nombre, codigo))

    nuevo_elemento = ET.fromstring(nuevo_contenido)

    clientes_creados = 0
    bancos_creados = 0
    clientes_actualizados = 0
    bancos_actualizados = 0

    for cliente_xml in nuevo_elemento.findall('.//cliente'):
        nit = cliente_xml.find('NIT').text.strip()
        if validar_nit(nit):
            if any(cliente.Nit_Cliente == nit for cliente in clientes):
                for cliente in clientes:
                    if cliente.Nit_Cliente == nit:
                        cliente.Nombre_Cliente = cliente_xml.find('nombre').text.strip()
                        clientes_actualizados += 1
                        break
            else:
                nombre = cliente_xml.find('nombre').text.strip()
                clientes.append(Cliente(nit, nombre))
                clientes_creados += 1
        else:
            print(f"NIT incorrecto: {nit}")

    for banco_xml in nuevo_elemento.findall('.//banco'):
        codigo = banco_xml.find('codigo').text.strip()
        if any(banco.Codigo_Banco == codigo for banco in bancos):
            for banco in bancos:
                if banco.Codigo_Banco == codigo:
                    banco.Nombre_Banco = banco_xml.find('nombre').text.strip()
                    bancos_actualizados += 1
                    break
        else:
            nombre = banco_xml.find('nombre').text.strip()
            bancos.append(Banco(nombre, codigo))
            bancos_creados += 1

    guardar_respuesta_config(RespuestaConfig(clientes_creados, bancos_creados, clientes_actualizados, bancos_actualizados))

    root = ET.Element('root')

    clientes_element = ET.SubElement(root, 'clientes')
    for cliente in clientes:
        cliente_element = ET.SubElement(clientes_element, 'cliente')
        ET.SubElement(cliente_element, 'NIT').text = cliente.Nit_Cliente
        ET.SubElement(cliente_element, 'nombre').text = cliente.Nombre_Cliente

    bancos_element = ET.SubElement(root, 'bancos')
    for banco in bancos:
        banco_element = ET.SubElement(bancos_element, 'banco')
        ET.SubElement(banco_element, 'codigo').text = banco.Codigo_Banco
        ET.SubElement(banco_element, 'nombre').text = banco.Nombre_Banco

    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    formatted_xml = remove_whitespace(xml_str)

    with open(archivo_guardado, 'w') as file:
        file.write(formatted_xml)

    return xml_str

def actualizar_base_datos_transaccion(archivo_guardado_transaccion, nuevo_contenido_transaccion):
    facturas = []
    pagos = []

    if os.path.exists(archivo_guardado_transaccion):
        tree = ET.parse(archivo_guardado_transaccion)
        root = tree.getroot()

        # Obtener todas las facturas del archivo XML
        for factura_xml in root.findall('.//factura'):
            numero_factura = factura_xml.find('numeroFactura').text.strip()
            nit_cliente = factura_xml.find('NITcliente').text.strip()
            fecha_factura = factura_xml.find('fecha').text.strip()
            valor_factura = factura_xml.find('valor').text.strip()
            facturas.append(Factura(numero_factura, nit_cliente, fecha_factura, valor_factura))

        # Obtener todos los pagos del archivo XML
        for pago_xml in root.findall('.//pago'):
            codigo_banco = pago_xml.find('codigoBanco').text.strip()
            fecha_pago = pago_xml.find('fecha').text.strip()
            nit_cliente = pago_xml.find('NITcliente').text.strip()
            valor_pago = pago_xml.find('valor').text.strip()
            pagos.append(Pago(codigo_banco, fecha_pago, nit_cliente, valor_pago))

    nuevo_elemento = ET.fromstring(nuevo_contenido_transaccion)

    facturas_creadas = 0
    facturas_duplicadas = 0
    facturas_error = 0
    pagos_creados = 0
    pagos_duplicados = 0
    pagos_error = 0

    for factura_xml in nuevo_elemento.findall('.//factura'):
        numero_factura = factura_xml.find('numeroFactura').text.strip()
        nit_cliente = factura_xml.find('NITcliente').text.strip()
        fecha_factura = factura_xml.find('fecha').text.strip()
        valor_factura = factura_xml.find('valor').text.strip()

        # Verificar si la factura ya existe
        if any(factura.Numero_Factura == numero_factura for factura in facturas):
            facturas_duplicadas += 1
        else:
            # Crear nueva factura
            facturas.append(Factura(numero_factura, nit_cliente, fecha_factura, valor_factura))
            facturas_creadas += 1

    for pago_xml in nuevo_elemento.findall('.//pago'):
        codigo_banco = pago_xml.find('codigoBanco').text.strip()
        fecha_pago = pago_xml.find('fecha').text.strip()
        nit_cliente = pago_xml.find('NITcliente').text.strip()
        valor_pago = pago_xml.find('valor').text.strip()

        # Verificar si el pago ya existe
        if any(pago.Codigo_Banco == codigo_banco and pago.Fecha_Pago == fecha_pago for pago in pagos):
            pagos_duplicados += 1
        else:
            # Crear nuevo pago
            pagos.append(Pago(codigo_banco, fecha_pago, nit_cliente, valor_pago))
            pagos_creados += 1

    guardar_respuesta_transaccion(RespuestaTranascion(facturas_creadas, facturas_duplicadas, facturas_error, pagos_creados, pagos_duplicados, pagos_error))

    root = ET.Element('transacciones')

    facturas_element = ET.SubElement(root, 'facturas')
    for factura in facturas:
        factura_element = ET.SubElement(facturas_element, 'factura')
        ET.SubElement(factura_element, 'numeroFactura').text = factura.Numero_Factura
        ET.SubElement(factura_element, 'NITcliente').text = factura.Nit_Cliente
        ET.SubElement(factura_element, 'fecha').text = factura.Fecha_Factura
        ET.SubElement(factura_element, 'valor').text = factura.Valor_Factura

    pagos_element = ET.SubElement(root, 'pagos')
    for pago in pagos:
        pago_element = ET.SubElement(pagos_element, 'pago')
        ET.SubElement(pago_element, 'codigoBanco').text = pago.Codigo_Banco
        ET.SubElement(pago_element, 'fecha').text = pago.Fecha_Pago
        ET.SubElement(pago_element, 'NITcliente').text = pago.Nit_Cliente
        ET.SubElement(pago_element, 'valor').text = pago.Valor_Pago

    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    formatted_xml = remove_whitespace(xml_str)

    with open(archivo_guardado_transaccion, 'w') as file:
        file.write(formatted_xml)

    return xml_str

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'archivo' not in request.files:
        return 'No se envió ningún archivo', 400

    archivo = request.files['archivo']

    if archivo.filename == '':
        return 'No se seleccionó ningún archivo', 400

    nuevo_contenido = archivo.read().decode('utf-8')

    nombre_archivo = 'Guardado_Config.xml'
    archivo_guardado = os.path.join(os.getcwd(), nombre_archivo)
    actualizar_base_datos(archivo_guardado, nuevo_contenido)

    return 'Archivo recibido y contenido guardado en Guardado_Config.xml', 200

@app.route('/uploadTransaccion', methods=['POST'])
def upload_transaction_file():
    if 'archivo' not in request.files:
        return 'No se envió ningún archivo', 400

    archivo = request.files['archivo']

    if archivo.filename == '':
        return 'No se seleccionó ningún archivo', 400

    nuevo_contenido_transaccion = archivo.read().decode('utf-8')

    nombre_archivo = 'Guardado_Transaccion.xml'
    archivo_guardado_transaccion = os.path.join(os.getcwd(), nombre_archivo)
    actualizar_base_datos_transaccion(archivo_guardado_transaccion, nuevo_contenido_transaccion)

    return 'Archivo recibido y contenido guardado en Guardado_Transaccion.xml', 200

@app.route('/reset', methods=['POST'])
def reset_data():
    nombre_archivo = 'Guardado_Config.xml'
    nombre_archivo2 = 'respuesta_config.xml'
    nombre_archivo3 = 'Guardado_Transaccion.xml'
    nombre_archivo4 = 'respuesta_transaccion.xml'
    archivo_guardado = os.path.join(os.getcwd(), nombre_archivo)
    #borra archivo de almacenamiento de Congifuracion
    if os.path.exists(archivo_guardado):
        os.remove(archivo_guardado)
    #borra archivo de almacenamiento de respuesta de Configuracion
    archivo_guardado2 = os.path.join(os.getcwd(), nombre_archivo2)
    if os.path.exists(archivo_guardado2):
        os.remove(archivo_guardado2)
    #borra archivo de almacenamiento de Transaccion
    archivo_guardado3 = os.path.join(os.getcwd(), nombre_archivo3)
    if os.path.exists(archivo_guardado3):
        os.remove(archivo_guardado3)
    #borra archivo de almacenamiento de respuesta de Transaccion
    archivo_guardado4 = os.path.join(os.getcwd(), nombre_archivo4)
    if os.path.exists(archivo_guardado4):
        os.remove(archivo_guardado4)

    

    return 'Datos reiniciados', 200

if __name__ == '__main__':
    app.run(port=4700, debug=True)
