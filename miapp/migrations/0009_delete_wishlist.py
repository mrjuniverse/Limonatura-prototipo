# Generated by Django 5.0.6 on 2024-06-14 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0008_alter_orderplaced_payment_wishlist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
