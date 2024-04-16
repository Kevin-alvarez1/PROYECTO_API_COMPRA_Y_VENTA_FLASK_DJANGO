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

def guardar_respuesta_config(respuesta):
    root = ET.Element('respuesta')

    clientes_element = ET.SubElement(root, 'clientes')
    if respuesta.clientes_creados is not None:
        ET.SubElement(clientes_element, 'creados').text = str(respuesta.clientes_creados)
    if respuesta.clientes_actualizados is not None:
        ET.SubElement(clientes_element, 'actualizados').text = str(respuesta.clientes_actualizados)

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
                        if cliente.Nombre_Cliente != cliente_xml.find('nombre').text.strip():
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
                    if banco.Nombre_Banco != banco_xml.find('nombre').text.strip():
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

if __name__ == '__main__':
    app.run(port=4700, debug=True)
