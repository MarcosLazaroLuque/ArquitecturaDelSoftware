<<<<<<< HEAD
from django.urls import path
from .views import lista_clientes, detalle_cliente

urlpatterns = [
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
=======
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion/', include('app_gestion_taller.urls')),
>>>>>>> 41263e665ae1dcc967eb641006b9b880fd8bc7eb
]