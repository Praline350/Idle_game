# Generated by Django 5.1 on 2024-08-23 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_set_polymorphic_ctype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={},
        ),
        migrations.RemoveField(
            model_name='item',
            name='polymorphic_ctype',
        ),
    ]