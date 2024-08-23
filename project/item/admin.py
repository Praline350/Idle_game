from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from item.models import Item, Food, Stuff, Ressource

# Admin pour le modèle parent (Item)
@admin.register(Item)
class ItemAdmin(PolymorphicParentModelAdmin):
    base_model = Item
    child_models = (Food, Stuff, Ressource)

# Admin pour les sous-classes concrètes
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', ]