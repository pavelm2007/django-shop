from cart.models import Order, OrderItem
from django.contrib import admin


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['name']}),
    ]
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
