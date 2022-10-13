from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    lat = models.DecimalField(max_digits=19, decimal_places=15, null=False, blank=False)
    lon = models.DecimalField(max_digits=19, decimal_places=15, null=False, blank=False)
    radius = models.FloatField(blank=False, null=False, default=0)
    tax = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.name
