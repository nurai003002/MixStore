from django.contrib import admin
from apps.secondary.models import Slider, Service, Team, Review
# Register your models here.

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_title', 'title', 'price')
    list_filter = ('title', )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'delivery', 'delivery_desc')
    list_filter = ('id', 'delivery')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')
    list_filter = ('id', 'name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position')
    list_filter = ('id', 'name')