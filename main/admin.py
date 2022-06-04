from django.contrib import admin

# Register your models here.

class Productadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

from .models import *

admin.site.register(Customer)
admin.site.register(Product,Productadmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)