
from django.utils import timezone
import math
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from .models import TracksLastPoints
from django.db.models import Q


class TracksPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TracksLastPoints
        fields = ('latitude','longitude','id_line','speed','time','id_mobile')


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def distance(data1, data2):
    p1_lat, p1_lon, p2_lat, p2_lon = [math.radians(c)
                                      for c in [data1['latitude'],
                                               data1['longitude'],
                                               data2.latitude,
                                               data2.longitude]
                                      ]
    numerator = math.sqrt(math.pow(math.cos(p2_lat) * math.sin(p2_lon - p1_lon), 2) + math.pow(math.cos(p1_lat) * math.sin(p2_lat) - math.sin(p1_lat) * math.cos(p2_lat) * math.cos(p2_lon - p1_lon), 2))
    denominator = (math.sin(p1_lat) * math.sin(p2_lat) + math.cos(p1_lat) * math.cos(p2_lat) * math.cos(p2_lon - p1_lon))
    # convert distance from radians to meters
    #  note: earth's radius ~ 6372800 meters
    # print 'distance:%s\n'%(math.atan2(numerator, denominator) * 6372800 )
    print('distance')
    return math.atan2(numerator, denominator) * 6372800


def save_data(data):
    serializer = TracksPointsSerializer(data=data)
    print('save')
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status=201)
    return JSONResponse(serializer.errors, status=400)


def delete_old_tracks():
    data = TracksLastPoints.objects.all()
    print(timezone.now())
    for i in data:
        print(i.time)
        dif = timezone.now() - i.time
        # print datetime.datetime.now(timezone.utc)
        print(dif.total_seconds() / 60)
        if (dif.total_seconds() / 60) > 5:
            TracksLastPoints.objects.filter(id=i.id).delete()
            print('deletando')


def verify_data(data):
    id_line = data['id_line']
    id_mobile = data['id_mobile']
    line = TracksLastPoints.objects.filter(id_line=id_line)
    if len(line) == 0:
        print('linha nova')
        return save_data(data)

    else:
        try:
            bus = TracksLastPoints.objects.get(Q(id_mobile=id_mobile), Q(id_line=id_line))
            if distance(data, bus) < 200:
                print('mesmo bus, apenas deleta')
                # necessito pensar se e interessante deletar pelo id_mobile ou somente pelo id
                TracksLastPoints.objects.get(Q(id_mobile=id_mobile), Q(id_line=id_line)).delete()
                return save_data(data)

            else:
                print("Outro bus")
                return save_data(data)

        except TracksLastPoints.DoesNotExist:
            for j in line:
                if distance(data, j) > 30:
                    print(" distancia maior que 30, usuarios na mesma linha mas em onibus diferente")
                    return save_data(data)
                    break
                else:
                    print("usuarios no mesmo onibus")
                    TracksLastPoints.objects.filter(id_mobile=j.id_mobile).delete()
                    return save_data(data)
                    break


@csrf_exempt
def go_bus_record(request):
    # tracks = []
    delete_old_tracks()
    if request.method == 'GET':
        tracks = TracksLastPoints.objects.all()
        print(tracks)
        serializer = TracksPointsSerializer(tracks, many=True)
        return JSONResponse(serializer.data)

    if request.method == 'POST':
        print('Post\n')
        data = JSONParser().parse(request)
        print('data:%s\n' % data['latitude'])
        aux = verify_data(data)
        return aux