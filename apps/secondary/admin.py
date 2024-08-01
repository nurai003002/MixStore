from django.contrib import admin
from apps.secondary.models import Slider, Service, Team
# Register your models here.

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'old_price')
    list_filter = ('title', )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'delivery_desc')
    list_filter = ('id', 'delivery')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')
    list_filter = ('id', 'name')
