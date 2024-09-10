from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from orders.models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    list_display = ['order', 'product', 'quantity', 'price']
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    model = Order
    list_display = ['user' , 'first_name' , 'last_name' , 'datetime_created' , 'is_paid']
    inlines = [
        OrderItemInline,
    ]
@admin.register(OrderItem)
class OrderItemAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ['order' , 'product' , 'quantity' , 'price']