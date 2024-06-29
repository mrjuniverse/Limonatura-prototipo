# Generated by Django 4.1.7 on 2024-06-12 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0003_alter_product_sku_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='miapp.cliente')),
            ],
        ),
    ]
