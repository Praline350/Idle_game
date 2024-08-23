from django.db import migrations
from django.contrib.contenttypes.models import ContentType

def set_polymorphic_ctype(apps, schema_editor):
    Item = apps.get_model('item', 'Item')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    for item in Item.objects.all():
        # Détermine la sous-classe de l'instance
        item_ct = ContentType.objects.get_for_model(item, for_concrete_model=False)
        # Met à jour le champ polymorphic_ctype
        item.polymorphic_ctype_id = item_ct.id
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_alter_item_options_item_polymorphic_ctype'),  # Remplace par la bonne migration précédente
    ]

    operations = [
        migrations.RunPython(set_polymorphic_ctype),
    ]
