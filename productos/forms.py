from django import forms
from .models import Producto, Venta, Usuario
from django import forms

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'sku', 'ean_upc', 'nombre', 'descripcion', 'categoria', 'marca', 'modelo',
            'uom_compra', 'uom_venta', 'factor_conversion', 'costo_estandar', 'costo_promedio', 'precio_venta', 'impuesto_iva',
            'stock', 'stock_minimo', 'stock_maximo', 'punto_reorden', 'perishable', 'control_por_lote', 'control_por_serie',
            'imagen_url', 'ficha_tecnica_url'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark required fields explicitly and set widget classes
        required_fields = ['sku', 'nombre', 'categoria', 'uom_compra', 'uom_venta', 'factor_conversion', 'impuesto_iva', 'stock_minimo']
        for fname, field in self.fields.items():
            if fname in required_fields:
                field.required = True
            # costo_promedio should be readonly in the form
            if fname == 'costo_promedio':
                field.disabled = True
            # set bootstrap classes
            if hasattr(field.widget, 'attrs'):
                if field.widget.__class__.__name__ == 'CheckboxInput':
                    field.widget.attrs.update({'class': 'form-check-input'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['total']
        widgets = {
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'nombres', 'apellidos', 'telefono',
            'rol', 'estado', 'mfa_habilitado', 'area', 'observaciones'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'mfa_habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
