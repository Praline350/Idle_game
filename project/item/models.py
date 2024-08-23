from django.db import models
from polymorphic.models import PolymorphicModel
from PIL import Image


MATERIAL_CHOICES = [
    ('leather', 'Leather'),
    ('copper', 'Copper'),
    ('iron', 'Iron'),
    ('gold', 'Gold'),
    ('mytril', 'Mytril')
]

STATS_CHOICES = [
    ('health', 'Health'),
    ('strength', 'Strength'),
    ('agility', 'Agility'),
    ('speed', 'Speed'),
    ('physical', 'Physical')
]

RARITY_CHOICES = [
    ('standard', 'Standard'),
    ('rare', 'rare')
]

class Item(PolymorphicModel):
    name = models.CharField(max_length=100)
    asset = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=300)
    price = models.PositiveIntegerField(default=1)
    rarity = models.CharField(max_length=30, choices=RARITY_CHOICES, default='standart')
        
    def __str__(self):
        return self.name
    

class Consumable(Item):
    affected_stat = models.CharField(max_length=50, choices=STATS_CHOICES)
    value = models.IntegerField()  # Value of stat to up 

    class Meta:
        abstract = True

    

class Stuff(Item):
    material = models.CharField(max_length=30, choices=MATERIAL_CHOICES)
    durability = models.PositiveIntegerField(default=100)
    
    class Meta:
        abstract = True 


class Ressource(Item):
    pass

    class Meta:
        abstract = True


class Food(Consumable):
    expire_in = models.PositiveIntegerField(default=5)