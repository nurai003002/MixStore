from django.contrib import admin
from apps.settings.models import Setting, About
# Register your models here.

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'phone')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')