from django.db import models
from PIL import Image



SKILL_CHOICES = [
    ('wooding', 'Wooding'),
    ('mining', 'Mining'),
    ('picking', 'Picking'),
    ('searching', 'Searching'),
]

class GeneralAction(models.Model):
    asset = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()  # Durée de l'action

    def __str__(self):
        return self.name


class FarmingAction(GeneralAction):
    reward_item = models.ForeignKey('item.Item', on_delete=models.SET_NULL, null=True, blank=True)
    reward_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    skill_updating = models.CharField(max_length=30, choices=SKILL_CHOICES,null=True, blank=True)
    value_updating = models.IntegerField(default=1)

    def perform(self, user):
        """Logique pour l'action de récolte."""

        character = user.character
        trailer = user.trailer
        # Mise à jour de la compétence du personnage
        if self.skill_updating:
            skill = getattr(character.general_skills, self.skill_updating)
            setattr(character.general_skills, self.skill_updating, skill + self.value_updating)
            character.general_skills.save()

        # Ajout des récompenses si applicable
        if self.reward_item:
            trailer.inventory.add_item(self.reward_item, self.reward_quantity)
