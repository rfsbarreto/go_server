from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from .models import Tracks, TracksPoints


class TracksPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TracksPoints
        fields = ('id','latitude','longitude','time')


class TracksSerializer(serializers.ModelSerializer):
    tracks_points = TracksPointsSerializer(many=True)

    class Meta:
        model = Tracks
        fields = ('id','id_android','time','distance','speed','rating','linha','car_or_bus','rating_weather','rating_bus','tracks_points')

    def create(self, validated_data):
        tracksPoints = validated_data.pop('tracks_points')
        tracks = Tracks.objects.create(**validated_data)

        for track in tracksPoints:
            TracksPoints.objects.create(track=tracks,**track)
        return tracks


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def go_track_record(request):

    if request.method == 'GET':
        tracks = Tracks.objects.all()
        serializer = TracksSerializer(tracks, many=True)
        return JSONResponse(serializer.data)

    if request.method == 'POST':

        data = JSONParser().parse(request)

        serializer = TracksSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
