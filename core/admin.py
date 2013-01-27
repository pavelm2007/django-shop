from core.models import Setting
from django.contrib import admin

class SettingAdmin(admin.ModelAdmin):
    list_per_page = 50

admin.site.register(Setting, SettingAdmin)
