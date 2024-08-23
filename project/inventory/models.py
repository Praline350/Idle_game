from django.db import models

class Inventory(models.Model):
    capacity = models.PositiveIntegerField(default=20)
    items = models.ManyToManyField('item.Item', through='inventory.InventoryItem')

    def add_item(self, item, quantity):
        if self.inventory_items.count() >= self.capacity:
            raise ValueError('Inventory Full')
        
        inventory_item, created = InventoryItem.objects.get_or_create(
            inventory=self, 
            item=item,
            defaults={'quantity': quantity}
        )
        if not created:
            inventory_item.quantity += quantity
            inventory_item.save()

    def remove_item(self, item, quantity):
        try:
            inventory_item = self.inventory_items.get(item=item)
            if inventory_item.quantity < quantity:
                raise ValueError('Not enought items to remove')
            inventory_item.quantity -= quantity
            if inventory_item.quantity == 0:
                inventory_item.delete()
            else: 
                inventory_item.save()
        except InventoryItem.DoesNotExist:
            raise ValueError('Item not found')

    def __str__(self):
        return f"Inventory with capacity {self.capacity}"


class InventoryItem(models.Model):
    inventory = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE, related_name='inventory_items')
    item = models.ForeignKey('item.Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inventory', 'item'], name='unique_inventory_item')
        ]

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"