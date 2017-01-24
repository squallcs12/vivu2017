from django.db import models


class Suggest(models.Model):
    address = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lng = models.DecimalField(max_digits=5, decimal_places=2)
    place_id = models.CharField(max_length=255, unique=True)
    province = models.CharField(max_length=80)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.address
