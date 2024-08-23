from django.db import models
from PIL import Image
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from inventory.models import *

SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]


class Stats(models.Model):
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=1)
    agility = models.IntegerField(default=1)
    speed = models.IntegerField(default=1)
    physical = models.IntegerField(default=1)

    def __str__(self):
        return f"Stats (Str: {self.strength}, Agi: {self.agility}, Spd: {self.speed}, Phy: {self.physical})"
    

class GeneralSkills(models.Model):
    wooding = models.IntegerField(default=1)
    mining = models.IntegerField(default=1)
    picking = models.IntegerField(default=1)
    searching = models.IntegerField(default=1)

    def __str__(self):
        return f"wood: {self.wooding},mining: {self.mining},picking: {self.picking}, searching: {self.searching}"


class Character(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='character')
    avatar = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    level = models.IntegerField(default=1)
    stats = models.OneToOneField(Stats, on_delete=models.CASCADE, related_name='character')
    general_skills = models.OneToOneField(GeneralSkills, on_delete=models.CASCADE, related_name='character')
    location =  models.ForeignKey('location.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name='characters')

    def save(self, *args, **kwargs):
        if not self.stats_id:
            self.stats = Stats.objects.create()
        if not self.general_skills_id:
            self.general_skills = GeneralSkills.objects.create()
        super().save(*args, **kwargs)

    def get_available_actions(self):
        # Retourne les actions disponible pour la position actuelle du joueur
        if self.location: 
            return self.location.get_location_actions()
        return []


    def __str__(self):
        return self.name


class Trailer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trailer', null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    inventory = models.OneToOneField('inventory.Inventory', on_delete=models.CASCADE,related_name='trailer')

    def save(self, *args, **kwargs):
        if not self.inventory_id:
            self.inventory = Inventory.objects.create()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name