from django import forms

from app_gestion_taller.models import Cliente, Coche, CocheServicio, Servicio

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = 'marca', 'modelo', 'matricula'

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = 'nombre', 'descripcion'

class CocheServicioForm(forms.ModelForm):
    class Meta:
        model = CocheServicio
        fields = '__all__'