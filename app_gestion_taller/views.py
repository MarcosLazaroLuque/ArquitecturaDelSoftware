<<<<<<< HEAD
from django.http import JsonResponse
from .models import Cliente

def lista_clientes(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 41263e665ae1dcc967eb641006b9b880fd8bc7eb
