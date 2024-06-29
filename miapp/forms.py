import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User, Group
from itertools import cycle
from .models import Cliente, Product, TCredito
from captcha.fields import CaptchaField

def validarRut(rut):
    rut = rut.upper()
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]
    
    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11
    
    if str(res) == dv:
        return True
    elif dv == "K" and res == 10:
        return True
    else:
        return False

def validate_rut(value):
    if not validarRut(value):
        raise ValidationError('El RUT no es válido.')


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='RUT', widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[validate_rut])
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
     
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.rut = self.cleaned_data['username']
        if commit:
            user.save()
            clientes_group, created = Group.objects.get_or_create(name='Clientes')
            user.groups.add(clientes_group)
        return user

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    captcha = CaptchaField()


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Contraseña Anterior', widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='Contraseña Nueva', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    #email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    pass

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'ciudad', 'region']
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'apellido':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'telefono':forms.NumberInput(attrs={'class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            'ciudad':forms.TextInput(attrs={'class':'form-control'}),
            'region':forms.Select(attrs={'class':'form-control'})
        }

class ProducAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nombre', 'precio', 'cantidad', 'descripcion', 'categoria', 'imagen_producto']
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'imagen_producto':forms.ClearableFileInput(attrs={'class':'form-control'}),
        }

class TCreditoForm(forms.ModelForm):
    class Meta:
        model = TCredito
        fields = ['nombre_completo', 'numero_tarjeta','cvv']
        widgets={
            'nombre_completo':forms.TextInput(attrs={'class':'form-control'}),
            'numero_tarjeta':forms.TextInput(attrs={'class':'form-control'}),
            'cvv':forms.TextInput(attrs={'class':'form-control'})
        }