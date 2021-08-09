from django.db import models
from django.contrib.gis.db.models import PolygonField
from django.contrib.postgres.fields import ArrayField

from providers.models import Provider


class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=255)
    price = models.DecimalField('Price', max_digits=15, decimal_places=5)
    coordinates = PolygonField()
