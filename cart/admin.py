from cart.models import Order, OrderItem
from django.contrib import admin


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_name', 'shipping_city', 'date', 'total', 'status')
    list_display_links = ('shipping_name',)
    list_filter = ('status', 'shipping_city', 'date')
    search_fields = ('email', 'shipping_name', 'billing_name', 'id', 'transaction_id')
    inlines = [OrderItemInline, ]
    fieldsets = (
        (None, {'fields':
                        ('email', 'phone', 'status'),
                'classes': ['wide', 'extrapretty']
                }),
        ('Shipping', {'fields':
                          ('shipping_name', 'shipping_address_1', 'shipping_address_2', 'shipping_city',
                           'shipping_state', 'shipping_zip', 'shipping_country')}),
        ('Billing', {'fields':
                         ('billing_name', 'billing_address_1', 'billing_address_2', 'billing_city', 'billing_state',
                          'billing_zip', 'billing_country'),
                     'classes': ('collapse',),
                    })
        )

admin.site.register(Order, OrderAdmin)

