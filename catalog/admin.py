from catalog.models import Product, Category, Option
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20

admin.site.register(Category, CustomMPTTModelAdmin)
admin.site.register(Option, CustomMPTTModelAdmin)
admin.site.register(Product)
