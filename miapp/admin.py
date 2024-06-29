from django.contrib import admin
from .models import Product, Cliente, Carrito, Payment, OrderPlaced

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','precio','cantidad','descripcion','sku','categoria','imagen_producto']

@admin.register(Cliente)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nombre', 'apellido', 'telefono', 'email', 'direccion', 'ciudad', 'region']

@admin.register(Carrito)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'producto', 'cantidad']

@admin.register(Payment)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'order_id', 'payment_status', 'payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']