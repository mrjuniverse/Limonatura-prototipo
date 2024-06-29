import random
from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.validators import MinLengthValidator

CATEGORY_CHOICES=(
    ('JO','Joyería de autor'),
    ('CA','Carteras'),
    ('VE','Vestimenta'),
    ('CZ','Calzado')
)

REGION_CHOICES=(
    ('Arica y Parinacota','Arica y Parinacota'),
    ('Tarapacá','Tarapacá'),
    ('Antofagasta','Antofagasta'),
    ('Atacama','Atacama'),
    ('Coquimbo','Coquimbo'),
    ('Valparaíso','Valparaíso'),
    ('Metropolitana de Santiago','Metropolitana de Santiago'),
    ('Libertador General Bernardo O’Higgins','Libertador General Bernardo O’Higgins'),
    ('Maule','Maule'),
    ('Ñuble','Ñuble'),
    ('Biobío','Biobío'),
    ('La Araucanía','La Araucanía'),
    ('Los Ríos','Los Ríos'),
    ('Los Lagos','Los Lagos'),
    ('Aysén del General Carlos Ibáñez del Campo','Aysén del General Carlos Ibáñez del Campo'),
    ('Magallanes y la Antártica Chilena','Magallanes y la Antártica Chilena'),
)

class Product(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    cantidad = models.IntegerField()
    descripcion = models.TextField()
    sku = models.IntegerField(unique=True, blank=True)
    categoria = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    imagen_producto = models.ImageField(upload_to='product')

    def __str__(self):
        return self.nombre
    
    def precio_formateado(self):
        return f"${intcomma(self.precio).replace(',', '.')}"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self.generate_unique_sku()
        super().save(*args, **kwargs)

    def generate_unique_sku(self):
        while True:
            sku = random.randint(1000000000, 9999999999)  # Genera un número de 10 dígitos
            if not Product.objects.filter(sku=sku).exists():
                return sku
            
class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    telefono = models.IntegerField(default=0)
    email = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=60)
    ciudad = models.CharField(max_length=30)
    region = models.CharField(choices=REGION_CHOICES, max_length=100)
    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def costo_total(self):
        return self.cantidad * self.producto.precio
    
STATUS_CHOICES = (
    ('Aceptado','Aceptado'),
    ('Preparando','Preparando'),
    ('En Camino','En Camino'),
    ('Entregado','Entregado'),
    ('Cancelado','Cancelado'),
    ('Pendiente','Pendiente'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    order_id=models.CharField(max_length=100, blank=True, null=True)
    payment_status=models.CharField(max_length=100, blank=True, null=True)
    payment_id=models.CharField(max_length=100, blank=True, null=True)
    tipopago = models.CharField(max_length=100, default="")
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    envio = models.IntegerField(default=5000)
    total_cost = models.IntegerField(blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")
    
    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.product.precio
        super().save(*args, **kwargs)
    
class TCredito(models.Model):
    nombre_completo = models.CharField(max_length=100, blank=True, null=True)
    numero_tarjeta = models.CharField(max_length=17, blank=True, null=True, validators=[MinLengthValidator(16)])
    cvv = models.CharField(max_length=10, blank=True, null=True)