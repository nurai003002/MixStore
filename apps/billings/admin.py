from django.contrib import admin

from apps.billings.models import Billings
# Register your models here.
@admin.register(Billings)
class BillingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    list_filter = ('id', 'first_name')