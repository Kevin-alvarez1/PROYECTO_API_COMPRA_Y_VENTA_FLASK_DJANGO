from django.urls import path
from . import views

urlpatterns=[
    path('', views.registrarCliente, name='registrarCliente'),
    path('Tabla', views.Tabla, name='Tabla'),

]