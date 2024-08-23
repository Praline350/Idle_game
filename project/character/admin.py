from django.contrib import admin

from character.models import *

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'level']

@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
