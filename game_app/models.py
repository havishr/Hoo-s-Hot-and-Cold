from django.db import models


# Create your models here.

class Game(models.Model):
    # Game name
    name = models.CharField(max_length=128)

    # Newly created Games should be approved by admins before they becom available
    is_approved = models.BooleanField(default=False)

    # Using 6 decimal places should be accurate enough
    # Google Maps API only gives 6
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
