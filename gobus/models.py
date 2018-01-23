from django.db import models

class TracksLastPoints(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    id_line = models.IntegerField()
    speed = models.FloatField()
    time = models.DateTimeField()
    id_mobile = models.CharField(max_length=50)

