from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.db import connection
import datetime as dt

from velocity.models import Tramos15MinUOCT, Status

# Create your views here.

class TimeMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        template = "velocity/map.html"

        return render(request, template, self.context)

class DiffMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        template = "velocity/mapDiff.html"

        return render(request, template, self.context)


class TimeTableMapHandler(View):
    '''  '''
    def __init__(self):
        self.context={}

    def get(self, request):
        template = 'velocity/table.html'

        return render(request, template, self.context)


class GetMapData(View):
    '''This class requests to the database the street secction with travel time '''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        """ streets data """
        points = Tramos15MinUOCT.objects.all().order_by('eje', 'tramo', 'dist_en_ruta')

        dest = 'Destination'
        response = {}
        response[dest] = {}
        for point in points:
            if not point.destino in response[dest]:
                response[dest][point.destino] = {}
            if not point.zona in response[dest][point.destino]:
                response[dest][point.destino][point.zona] = {}
            if not point.eje in response[dest][point.destino][point.zona]:
                street = {}
                street['origin'] = point.hito_origen
                street['destination'] = point.hito_destino
                street['sections'] = {}
                response[dest][point.destino][point.zona][point.eje] = street
             
            if not point.tramo in response[dest][point.destino][point.zona][point.eje]['sections']:
                section = {}
                section['id'] = "{0}-{1}".format(point.eje_id.encode('utf-8'), point.secuencia_eje_macro)
                section['name'] = point.secuencia_eje_macro
                section['originStreet'] = point.calle_origen
                section['destinationStreet'] = point.calle_destino
                section['nObs'] = point.nobs
                section['group'] = point.grupo
                section['segxkm'] = point.segundos_por_km_tramo
                section['diff'] = point.diferencia_referencia
                section['points'] = []
                response[dest][point.destino][point.zona][point.eje]['sections'][point.tramo] = section

            response[dest][point.destino][point.zona][point.eje]['sections'][point.tramo]['points'].append({
                'distOnRoute': point.dist_en_ruta, 
                'latitude': point.latitud, 
                'longitude': point.longitud})

        hour = None
        dayType = None
        if point:
            delta = dt.timedelta(minutes=15)
            upperTimeLimit = (dt.datetime.combine(dt.date.today(), point.periodo15) + delta).time()
            hour = "{}-{}".format(point.periodo15, upperTimeLimit)
            dayType = point.tipo_dia

        response['hour'] = hour
        response['dayType'] = dayType

        return JsonResponse(response, safe=False)

class GetTimeTableData(View):
    ''' '''

    def __init__(self):
        ''' '''
        self.context={}

    def get(self, request):
        ''' '''
        points = Tramos15MinUOCT.objects.all().distinct('eje_id', 'tramo', 'calle_origen', 'calle_destino', 'segundos_por_km_tramo')

        dataset = []
        for point in points:
            street = {}
            street['axis'] = point.eje_id
            street['section'] = point.secuencia_eje_macro
            street['origin'] = point.calle_origen
            street['destination'] = point.calle_destino
            street['metrics'] = point.segundos_por_km_tramo
            street['diff'] = point.diferencia_referencia

            dataset.append(street)

        response = {}
        response['dataset'] = dataset
        response['hour'] = ''
        if point:
            delta = dt.timedelta(minutes=15)
            upperTimeLimit = (dt.datetime.combine(dt.date.today(), point.periodo15) + delta).time()
            response['hour'] = "{}-{}".format(point.periodo15, upperTimeLimit)

        return JsonResponse(response, safe=False)


class GetDataStatus(View):
    ''' '''

    def __init___(self):
        ''' '''
        self.context = {}

    def get(self, request):
        ''' '''
        obj = Status.objects.get(id='uoct1')

        response = {}
        response['status'] = obj.status

        return JsonResponse(response, safe=False)

