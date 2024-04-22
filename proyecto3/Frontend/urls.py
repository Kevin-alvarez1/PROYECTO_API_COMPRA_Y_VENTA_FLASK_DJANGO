from django.urls import path
from . import views

urlpatterns=[
    path('', views.registrarCliente, name='registrarCliente'),
    path('Consultar_cuenta', views.Consultar_cuenta, name='Consultar_cuenta'),
    path('Consultar_Ingresos', views.Consultar_Ingresos, name='Consultar_Ingresos'),
    path('Cargar_Config', views.Cargar_Config, name='Cargar_Config'),
    path('Cargar_Transac', views.Cargar_Transac, name='Cargar_Transac'),
    path('Peticiones', views.Peticiones, name='Peticiones'),
    path('Resetear_datos', views.Resetear_datos, name='Resetear_datos'),
    path('Ayuda', views.Ayuda, name='Ayuda'),
    path('Info_Estudiante', views.Info_Estudiante, name='Info_Estudiante'),
    path('Info_pagina', views.Info_pagina, name='Info_pagina'),
    path('upload', views.upload_to_flask, name='upload_to_flask'),
    path('reset', views.reset_to_flask, name='reset_to_flask'),
    path('uploadTransaccion', views.upload_transaccion_to_flask, name='upload_transaccion_to_flask'),
    path('tabla-clientes', views.tabla_clientes, name='tabla-clientes'),
    path('Seleccionar_Cliente', views.Seleccionar_Cliente, name='Seleccionar_Cliente'),

]