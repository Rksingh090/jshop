from django.contrib import admin
from .models import Product, Cart, Orders

# Register your models here.

class productAdmin(admin.ModelAdmin):
    list_display = ['productName', 'productPrize']
admin.site.register(Product, productAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display = ['productName', 'id','userId', 'productPrize']
admin.site.register(Cart, cartAdmin)

class orderAdmin(admin.ModelAdmin):
    list_filter = ['paymentStatus']
    list_display = ['userName','orderId', 'paymentStatus', 'city', 'zip_code']
admin.site.register(Orders, orderAdmin)

