from django.urls import path
from .views import lista_clientes, detalle_cliente
from .views import crear_cliente, crear_coche, crear_servicio
from .views import obtener_cliente, obtener_servicios_coche, obtener_coche_cliente, obtener_coche_matricula

urlpatterns = [
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
    path('clientes/crear/', crear_cliente, name='crear_cliente'),
    path('coches/crear/', crear_coche, name='crear_coche'),
    path('servicios/crear/', crear_servicio, name='crear_servicio'),
    path('coches/matricula/<str:matricula>/', obtener_coche_matricula, name='obtener_coche_matricula'),
    path('clientes/<int:cliente_id>/coches/', obtener_coche_cliente, name='obtener_coche_cliente'),
    path('coches/<int:coche_id>/servicios/', obtener_servicios_coche, name='obtener_servicios_coche'),
]