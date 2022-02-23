from django.contrib import admin
from .models import Product, Cart

# Register your models here.

class productAdmin(admin.ModelAdmin):
    list_display = ['id', 'productName', 'productPrize']
admin.site.register(Product, productAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display = ['productName', 'id','userId', 'productPrize']
admin.site.register(Cart, cartAdmin)