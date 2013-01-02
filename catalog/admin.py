from catalog.models import Product, Category, Option
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class OptionMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    list_display = ('name', 'slug', 'is_active', 'count_products')
    mptt_level_indent = 20
    actions = ['hide_category', 'un_hide_category']

    def hide_category(self, request, queryset):
        rows_updated = queryset.update(hidden=True)
        if rows_updated == 1:
            message_bit = "1 category was"
        else:
            message_bit = "%s categories were" % rows_updated
        self.message_user(request, "%s successfully marked as hidden." % message_bit)

    def un_hide_category(self, request, queryset):
        rows_updated = queryset.update(hidden=False)
        if rows_updated == 1:
            message_bit = "1 category was"
        else:
            message_bit = "%s categories were" % rows_updated
        self.message_user(request, "%s successfully marked as active." % message_bit)

    un_hide_category.short_description = "Mark selected as active"
    hide_category.short_description = "Mark selected as hidden"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price')
    search_fields = ['slug', 'price']

admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Option, OptionMPTTModelAdmin)
