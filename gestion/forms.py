from django import forms
from .models import Cliente, Cuenta, Transaccion


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'rut']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['cliente', 'tipo', 'saldo']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta_origen', 'cuenta_destino', 'tipo', 'monto', 'descripcion']
        widgets = {
            'cuenta_origen': forms.Select(attrs={'class': 'form-control'}),
            'cuenta_destino': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Opcional'}),
        }
