from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model

from character.models import *
from location.models import *
from action.models import *

User = get_user_model()

class LocationTest(TestCase):

    def setUp(self):
        # Crée des types de lieux
        self.forest_type = LocationType.objects.create(name="Forêt", description="Un lieu boisé.")
        self.village_type = LocationType.objects.create(name="Village", description="Un petit village paisible.")

        # Crée des lieux
        self.forest = Location.objects.create(name="Forêt Sombre", location_type=self.forest_type)
        self.village = Location.objects.create(name="Village des Montagnes", location_type=self.village_type)

        # Crée une action générique
        self.action = GeneralAction.objects.create(name="Couper du bois", description="Coupez des arbres pour récolter du bois.", duration=timedelta(minutes=5))

        # Associe l'action à un lieu
        self.forest.general_actions.add(self.action)

        # Créer un personnage
        self.user = User.objects.create_user(username="Test_user", password='12345')
        self.character = Character.objects.create(user=self.user, name='Hero', age=20, sex='M', location=self.forest)
    

    def test_location_creation(self):
        # Vérifie que les lieux sont bien créés
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(self.forest.name, "Forêt Sombre")
        self.assertEqual(self.village.name, "Village des Montagnes")

    def test_location_type(self):
        # Vérifie que les lieux sont associés au bon type
        self.assertEqual(self.forest.location_type, self.forest_type)
        self.assertEqual(self.village.location_type, self.village_type)

    def test_location_actions(self):
        # Vérifie que l'action est bien associée à la forêt
        self.assertIn(self.action, self.forest.get_location_actions())
        self.assertNotIn(self.action, self.village.get_location_actions())

    def test_location_connections(self):
        # Connecte deux lieux et vérifie la connexion
        self.forest.connected_locations.add(self.village)
        self.assertIn(self.village, self.forest.connected_locations.all())
        self.assertIn(self.forest, self.village.connected_locations.all())

    def test_get_available_actions_in_forest(self):
        actions = self.character.get_available_actions()  # Utilisation de la méthode sur Character
        self.assertIn(self.action, actions)

    def test_get_available_actions_in_village(self):
        # Change la location du personnage au village où il n'y a pas d'action
        self.character.location = self.village
        self.character.save()

        actions = self.character.get_available_actions()
        self.assertNotIn(self.action, actions)  # L'action ne doit pas être disponible