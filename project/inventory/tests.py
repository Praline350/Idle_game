from django.test import TestCase
from django.contrib.auth import get_user_model

from character.models import *
from inventory.models import *
from item.models import *

User= get_user_model()

class InventoryTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.character = Character.objects.create(user=self.user, name='Hero', age=20, sex='M')
        self.trailer = Trailer.objects.create(user=self.user, name='My trailer')
        self.item1 = Item.objects.create(name='sword', description='Test')
        self.item2 = Item.objects.create(name='apple', description='Test2')

    def test_inventory_exist(self):
        self.assertIsNotNone(self.trailer.inventory)

    def test_add_item(self):
        self.trailer.inventory.add_item(self.item1, 1)
        self.assertEqual(self.trailer.inventory.inventory_items.count(), 1)
        self.assertEqual(self.trailer.inventory.inventory_items.first().item, self.item1)
        self.assertEqual(self.trailer.inventory.inventory_items.first().quantity, 1)

    def test_add_existing_item(self):
        # Ajoute un item deux fois
        self.trailer.inventory.add_item(self.item1, 1)
        self.trailer.inventory.add_item(self.item1, 2)

        # Vérifie que la quantité a été mise à jour
        inventory_item = self.trailer.inventory.inventory_items.get(item=self.item1)
        self.assertEqual(inventory_item.quantity, 3)

    def test_add_item_inventory_full(self):
        # Ajoute deux items pour remplir l'inventaire
        self.trailer.inventory.capacity = 2
        self.trailer.inventory.add_item(self.item1, 1)
        self.trailer.inventory.add_item(self.item2, 1)
        
        # Tente d'ajouter un autre item, ce qui devrait lever une exception
        with self.assertRaises(ValueError) as e:
            self.trailer.inventory.add_item(self.item1, 1)
        
        self.assertEqual(str(e.exception), 'Inventory Full')

    def test_remove_item(self):
        # Ajoute un item et ensuite le retire
        self.trailer.inventory.add_item(self.item1, 3)
        self.trailer.inventory.remove_item(self.item1, 2)

        # Vérifie que la quantité a été mise à jour
        inventory_item = self.trailer.inventory.inventory_items.get(item=self.item1)
        self.assertEqual(inventory_item.quantity, 1)

    def test_remove_item_quantity_more_than_available(self):
        # Ajoute un item
        self.trailer.inventory.add_item(self.item1, 1)

        # Tente de retirer une quantité plus grande que disponible
        with self.assertRaises(ValueError) as e:
            self.trailer.inventory.remove_item(self.item1, 2)
        
        self.assertEqual(str(e.exception), 'Not enought items to remove')

    def test_remove_item_completely(self):
        # Ajoute un item et ensuite le retire complètement
        self.trailer.inventory.add_item(self.item1, 1)
        self.trailer.inventory.remove_item(self.item1, 1)

        # Vérifie que l'item a été supprimé de l'inventaire
        with self.assertRaises(InventoryItem.DoesNotExist):
            self.trailer.inventory.inventory_items.get(item=self.item1)

    def test_remove_item_not_found(self):
        # Tente de retirer un item qui n'existe pas dans l'inventaire
        with self.assertRaises(ValueError) as e:
            self.trailer.inventory.remove_item(self.item1, 1)
        
        self.assertEqual(str(e.exception), 'Item not found')
