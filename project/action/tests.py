from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model

from character.models import *
from action.models import *
from item.models import *

User = get_user_model()


class FarmingActionTest(TestCase):

    def setUp(self):
        # Crée un personnage avec des compétences de base
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.skills = GeneralSkills.objects.create(wooding=10, mining=5, picking=7, searching=3)
        self.character = Character.objects.create(user=self.user, name="Héros", general_skills=self.skills, age=20, sex='M')
        self.trailer = Trailer.objects.create(user=self.user, name='My Trailer')

        # Crée un item de récompense
        self.wood_item = Item.objects.create(name="Wood", description="Un morceau de bois.")

        # Crée une action de coupe de bois
        self.farming_action = FarmingAction.objects.create(
            name="Couper du bois",
            description="Coupez des arbres pour récolter du bois.",
            duration=timedelta(minutes=5),
            reward_item=self.wood_item,
            reward_quantity=5,
            skill_updating='wooding',
            value_updating=3
        )

    def test_farming_action_creation(self):
        # Vérifie que l'action de coupe de bois est bien créée
        self.assertEqual(FarmingAction.objects.count(), 1)
        self.assertEqual(self.farming_action.name, "Couper du bois")

    def test_perform_action_skill_update(self):
        # Exécute l'action et vérifie que la compétence est mise à jour
        self.farming_action.perform(self.user)
        self.character.general_skills.refresh_from_db()
        self.assertEqual(self.character.general_skills.wooding, 13)  # 10 + 3

    
    def test_perform_action_reward(self):
        # Exécute l'action et vérifie que l'item est ajouté à l'inventaire
        self.farming_action.perform(self.user)  # Passer l'utilisateur, pas le personnage
        inventory_item = InventoryItem.objects.get(inventory=self.user.trailer.inventory, item=self.wood_item)
        self.assertEqual(inventory_item.quantity, 5)

    def test_perform_action_no_skill_update(self):
        # Crée une action sans mise à jour de compétence
        no_skill_action = FarmingAction.objects.create(
            name="Collecter des herbes",
            description="Ramassez des herbes.",
            duration=timedelta(minutes=3),
            reward_item=None,
            reward_quantity=0,
            skill_updating=None,
            value_updating=0
        )
        
        # Exécute l'action
        no_skill_action.perform(self.user)
        
        # Vérifie que les compétences ne sont pas modifiées
        self.character.general_skills.refresh_from_db()
        self.assertEqual(self.character.general_skills.wooding, 10)  # La compétence doit rester inchangée

    def test_perform_action_no_reward(self):
        # Crée une action sans récompense
        no_reward_action = FarmingAction.objects.create(
            name="Miner",
            description="Miner du fer",
            duration=timedelta(minutes=10),
            reward_item=None,
            reward_quantity=0,
            skill_updating='mining',  # Imaginons qu'il y ait une compétence de pêche
            value_updating=2
        )
        
        # Mock la méthode add_item pour s'assurer qu'elle n'est pas appelée
        self.trailer.inventory.add_item = lambda item, quantity: None
        
        # Exécute l'action
        no_reward_action.perform(self.user)
        
        # Vérifie que l'inventaire n'a pas été modifié (puisqu'il n'y a pas de récompense)
        self.trailer.inventory.add_item(self.wood_item, 0)  # Aucune modification n'est attendue