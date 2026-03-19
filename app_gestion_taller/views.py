from django.http import JsonResponse

from app_gestion_taller.forms import ClienteForm, CocheForm, ServicioForm, CocheServicioForm
from .models import Cliente
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Coche, Servicio, CocheServicio
import json
from django.shortcuts import redirect, render

def lista_clientes(request):
    #clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    #return JsonResponse(clientes, safe=False)
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_taller/lista_clientes.html', {'clientes': clientes})

def detalle_cliente(request, cliente_id):
    try:
        #cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        #return JsonResponse(cliente)
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)
        context = {
            'cliente': cliente,
            'coches': coches
        }
        return render(request, 'app_gestion_taller/detalle_cliente.html', context)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)


@csrf_exempt
def crear_cliente(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data["nombre"],
                telefono=data["telefono"],
                email=data["email"]
            )
            return JsonResponse({"mensaje": cliente.nombre + " creado exitosamente", "cliente": {"id": cliente.id, "nombre": cliente.nombre, "telefono": cliente.telefono, "email": cliente.email}})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def crear_coche(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data["cliente_id"])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data["marca"],
                modelo=data["modelo"],
                matricula=data["matricula"]
            )
            return JsonResponse({"mensaje": coche.marca + " " + coche.modelo + " creado exitosamente", "coche": {"id": coche.id, "cliente_id": coche.cliente.id, "marca": coche.marca, "modelo": coche.modelo, "matricula": coche.matricula}})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def crear_servicio(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data["coche_id"])
            servicio = Servicio.objects.create(
                nombre=data["nombre"],
                descripcion=data["descripcion"]
            )
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": servicio.nombre + " creado exitosamente", "servicio": {"id": servicio.id, "nombre": servicio.nombre, "descripcion": servicio.descripcion}})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def obtener_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    
@csrf_exempt
def obtener_coche_matricula(request, matricula):
    try:
        coche = Coche.objects.select_related('cliente').get(matricula=matricula)
        respuesta = {
            "coche": {
                "id": coche.id,
                "marca": coche.marca,
                "modelo": coche.modelo,
                "matricula": coche.matricula,
            },
            "cliente": {
                "id": coche.cliente.id,
                "nombre": coche.cliente.nombre,
                "telefono": coche.cliente.telefono,
                "email": coche.cliente.email,
            }
        }
        return JsonResponse(respuesta)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)
    
@csrf_exempt
def obtener_coche_cliente(request, cliente_id):
    try:
        coches = list(Coche.objects.filter(cliente_id=cliente_id).values("id", "marca", "modelo", "matricula"))
        return JsonResponse(coches, safe=False)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    
@csrf_exempt
def obtener_servicios_coche(request, coche_id):
    try:
        #servicios = list(CocheServicio.objects.filter(coche=coche).select_related('servicio').values("servicio__id", "servicio__nombre", "servicio__descripcion", "fecha"))
        #respuesta = {
        #    "coche": {
        #        "id": coche.id,
        #        "marca": coche.marca,
        #        "modelo": coche.modelo,
        #        "matricula": coche.matricula,
        #    },
        #    "servicios": servicios,
        #}
        #return JsonResponse(respuesta)
        coche = Coche.objects.get(id=coche_id)
        coche_servicios = CocheServicio.objects.filter(coche=coche).select_related('servicio')
        context = {
            'coche': coche,
            'coche_servicios': coche_servicios
        }
        return render(request, 'app_gestion_taller/servicios_coche.html', context)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'app_gestion_taller/formulario.html', {'form': form, 'titulo': 'Nuevo Cliente'})

def nuevo_coche(request, cliente_id):
    if request.method == 'POST':
        form = CocheForm(request.POST)
        cliente = Cliente.objects.get(id=cliente_id)
        if form.is_valid():
            Coche.objects.create(
                cliente=cliente,
                marca=form.cleaned_data['marca'],
                modelo=form.cleaned_data['modelo'],
                matricula=form.cleaned_data['matricula'],
            )
        
            return redirect('detalle_cliente', cliente_id=cliente_id)
    else:
        form = CocheForm()
    return render(request, 'app_gestion_taller/formulario.html', {'form': form, 'titulo': 'Nuevo Coche'})


def nuevo_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ServicioForm()
    return render(request, 'app_gestion_taller/formulario.html', {'form': form, 'titulo': 'Nuevo Servicio'})


def nuevo_servicio_coche(request):
    if request.method == 'POST':
        form = CocheServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('obtener_servicios_coche', coche_id=form.cleaned_data['coche'].id)
    else:
        form = CocheServicioForm()
    return render(request, 'app_gestion_taller/formulario.html', {'form': form, 'titulo': 'Nuevo Servicio para Coche'})
