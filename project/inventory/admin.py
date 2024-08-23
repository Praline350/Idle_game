from django.contrib import admin

from inventory.models import *

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['capacity',]
