from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
