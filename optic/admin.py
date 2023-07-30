from django.contrib import admin
from .models import Client, Seller, Product, Brand, Category, Cart, ActionCounter, ClientCounter, SaleCounter
# Register your models here.


admin.site.register(Client)
admin.site.register(Seller)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ActionCounter)
admin.site.register(ClientCounter)
admin.site.register(SaleCounter)