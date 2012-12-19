from catalog.models import Product, Category, Option
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class OptionMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20

class CategoryMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    list_display = ('name', 'slug', 'count_products')
    mptt_level_indent = 20


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price')
    search_fields = ['slug', 'price']

admin.site.register(Product, ProductAdmin)


admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Option, OptionMPTTModelAdmin)
