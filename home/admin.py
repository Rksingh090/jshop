from django.contrib import admin
from .models import ContactUs, Product, Cart, Orders

# Register your models here.

class productAdmin(admin.ModelAdmin):
    list_display = ['productName', 'productPrize']
admin.site.register(Product, productAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display = ['productName', 'id','userId', 'productPrize', "orderId"]
admin.site.register(Cart, cartAdmin)

class orderAdmin(admin.ModelAdmin):
    list_filter = ['paymentStatus']
    list_display = ['userName','orderId', 'paymentStatus', 'city', 'zip_code']
admin.site.register(Orders, orderAdmin)


class contactAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'message']
admin.site.register(ContactUs, contactAdmin)

