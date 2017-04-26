from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.db import connection
import datetime as dt

from velocity.models import Tramos15MinUOCT

# Create your views here.

class StreetVelocityMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        template = "velocity/map.html"

        return render(request, template, self.context)

class StreetVelocityDiffMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        template = "velocity/mapDiff.html"

        return render(request, template, self.context)


class StreetTimeTableMapHandler(View):
    '''  '''
    def __init__(self):
        self.context={}

    def get(self, request):
        template = 'velocity/table.html'

        return render(request, template, self.context)


class GetStreetData(View):
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
                #street['name'] = point.eje
                street['origin'] = point.hito_origen
                street['destination'] = point.hito_destino
                #street['group'] = point.zona
                #street['zoneGoal'] = point.destino
                #street['velocity'] = point.velocidad_eje
                #street['time'] = point.tiempo_viaje_eje
                street['sections'] = {}
                response[dest][point.destino][point.zona][point.eje] = street
             
            if not point.tramo in response[dest][point.destino][point.zona][point.eje]['sections']:
                section = {}
                section['originStreet'] = point.calle_origen
                section['destinationStreet'] = point.calle_destino
                section['nObs'] = point.nobs
                section['group'] = point.grupo
                section['segxkm'] = point.segundos_por_km_tramo
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

class GetStreetDiffData(View):
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
                section['originStreet'] = point.calle_origen
                section['destinationStreet'] = point.calle_destino
                section['nObs'] = point.nobs
                section['group'] = point.grupo
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



class GetStreetTableData(View):
    ''' '''

    def __init__(self):
        ''' '''
        self.context={}

    def get(self, request):
        ''' '''
        points = Tramos15MinUOCT.objects.all().distinct('eje_id', 'tramo', 'calle_origen', 'calle_destino', 'segundos_por_km_tramo')

        response = []
        for point in points:
            street = {}
            street['axis'] = point.eje_id
            street['section'] = point.tramo
            street['origin'] = point.calle_origen
            street['destination'] = point.calle_destino
            street['metrics'] = point.segundos_por_km_tramo

            response.append(street)

        return JsonResponse(response, safe=False)
