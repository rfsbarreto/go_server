from django.db import models


class Tracks(models.Model):
    id = models.AutoField(primary_key=True)
    id_android = models.CharField(max_length=32)
    time = models.FloatField()
    distance = models.FloatField()
    speed = models.FloatField()
    rating = models.IntegerField()
    linha = models.CharField(max_length=32)
    car_or_bus = models.IntegerField()
    rating_weather = models.IntegerField()
    rating_bus = models.IntegerField()


class TracksPoints(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    track = models.ForeignKey(Tracks, related_name='tracks_points')
    time = models.DateTimeField()

