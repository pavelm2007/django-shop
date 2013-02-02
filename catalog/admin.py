from catalog.models import Product, ProductMedia, Category, Option
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from imperavi.admin import ImperaviAdmin
from imperavi.admin import ImperaviStackedInlineAdmin
from feincms.admin import tree_editor


class OptionMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20


class CategoryMPTTModelAdmin(tree_editor.TreeEditor):
    # specify pixel amount for this ModelAdmin only:
    list_display = ('name', 'slug', 'is_active', 'count_products')
    mptt_level_indent = 20
    actions = ['hide_category', 'un_hide_category']
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug' : ('name',)}

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


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 0

class ProductAdmin(ImperaviAdmin):
    list_display = ('name', 'price', 'old_price', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']

    # sets up slug to be generated from product name
    prepopulated_fields = {'slug' : ('name',)}

    inlines = [ProductMediaInline]

admin.site.register(Product, ProductAdmin)

admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Option, OptionMPTTModelAdmin)
