from catalog.models import Product, Category, Option
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class OptionMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20

# Categories
def hide_category(modelAdmin, request, queryset):
    queryset.update(hidden=True)


def un_hide_category(modelAdmin, request, queryset):
    queryset.update(hidden=False)

un_hide_category.short_description = "Mark selected stories as active"
hide_category.short_description = "Mark selected stories as hidden"

class CategoryMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    list_display = ('name', 'slug', 'is_active', 'count_products')
    mptt_level_indent = 20
    actions = [hide_category, un_hide_category]


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price')
    search_fields = ['slug', 'price']

admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Option, OptionMPTTModelAdmin)
