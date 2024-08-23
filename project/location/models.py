from django.db import models


class LocationType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Location(models.Model):
    asset = models.ImageField(blank=True, null=True)
    name = models.CharField(max_length=100)
    location_type = models.ForeignKey(LocationType, on_delete=models.CASCADE, related_name='locations')
    description = models.TextField()
    connected_locations = models.ManyToManyField('self', blank=True)  # Lieux connectés
    general_actions = models.ManyToManyField('action.GeneralAction', related_name='locations', blank=True)

    def __str__(self):
        return self.name

    def get_location_actions(self):
        # Retourne les actions disponibles pour ce lieu
        return self.general_actions.all()

