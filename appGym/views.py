from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'gym/index.html')

def usuarios(request):
    return render(request, 'gym/usuarios.html')

def entradas_salidas(request):
    return render(request, 'gym/entradas_salidas.html')

def reportes(request):
    return render(request, 'gym/reportes.html')

def membresias(request):
    return render(request, 'gym/membresias.html')

def observaciones(request):
    return render(request, 'gym/observaciones.html')