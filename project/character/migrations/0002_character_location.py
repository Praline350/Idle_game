# Generated by Django 5.1 on 2024-08-23 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', to='location.location'),
        ),
    ]
