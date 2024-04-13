from django.shortcuts import render

# Create your views here.
def registrarCliente(request):
    return render(request, 'registrarCliente.html')
def Tabla(request):
    return render(request, 'Tabla.html')