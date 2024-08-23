from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Character, Trailer

User= get_user_model()


class CharacterTrailerCreationTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')

    def test_create_character(self):
        # Test pour créer un personnage lié à l'utilisateur
        character = Character.objects.create(user=self.user, name='Hero', age=20, sex='M')
        self.assertEqual(character.user, self.user)
        self.assertEqual(character.name, 'Hero')
        self.assertEqual(character.level, 1)
        self.assertIsNotNone(self.user.character)

    def test_create_trailer(self):
        # Test pour créer un trailer lié à l'utilisateur
        trailer = Trailer.objects.create(user=self.user, name='My Trailer')
        self.assertEqual(trailer.user, self.user)
        self.assertEqual(trailer.name, 'My Trailer')
        self.assertIsNotNone(self.user.trailer)
        self.assertIsNotNone(trailer.inventory)
        

    def test_user_relations(self):
        # Test pour vérifier les relations du User
        character = Character.objects.create(user=self.user, name='Hero', age=20,  sex=20)
        trailer = Trailer.objects.create(user=self.user, name='My Trailer')

        self.assertEqual(self.user.character, character)
        self.assertEqual(self.user.trailer, trailer)