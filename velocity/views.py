from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.db import connection
import datetime as dt

from velocity.models import Tramos15MinUOCT74, Tramos15MinUOCT2349, Tramos15MinUOCTReferencia74, Tramos15MinUOCTReferencia2349, Status

# Create your views here.
def transformData(points):
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
            section['order'] = point.secuencia_eje_macro
            section['originStreet'] = point.calle_origen
            section['destinationStreet'] = point.calle_destino
            section['nObs'] = point.nobs
            section['group'] = point.grupo
            section['segxkm'] = point.segundos_por_km_tramo
            section['diff'] = point.diferencia_referencia
            section['percDiff'] = point.coeficiente_referencia
            if hasattr(point, 'vel_referencia'):
                section['preVelRef'] = point.vel_referencia
            if hasattr(point, 'vel_referenciapost'):
                section['posVelRef'] = point.vel_referenciapost
            if hasattr(point, 'vel_referenciadiff'):
                section['diffVelRef'] = point.vel_referenciadiff
            section['points'] = []
            response[dest][point.destino][point.zona][point.eje]['sections'][point.tramo] = section

        response[dest][point.destino][point.zona][point.eje]['sections'][point.tramo]['points'].append({
            'distOnRoute': point.dist_en_ruta, 
            'latitude': point.latitud, 
            'longitude': point.longitud})

    return response


class RefMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request, networkId):
        template = "velocity/refMap.html"
        networkId = int(networkId)
        self.context['networkId'] = networkId

        entity = None
        if networkId ==  741:
            entity = Tramos15MinUOCTReferencia74
        elif networkId == 23491:
            entity = Tramos15MinUOCTReferencia2349
 
        self.context['dayTypes'] = entity.objects.values_list('tipodia', flat=True).distinct().order_by('tipodia')
        self.context['periods'] = entity.objects.values_list('periodo15', flat=True).distinct().order_by('periodo15')

        return render(request, template, self.context)


class TimeMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request, networkId):
        template = "velocity/map.html"
        self.context['networkId'] = networkId

        return render(request, template, self.context)

class DiffMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request, networkId):
        template = "velocity/mapDiff.html"
        self.context['networkId'] = networkId

        return render(request, template, self.context)

class PercDiffMapHandler(View):
    '''This class manages the map where the street section are shown'''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request, networkId):
        template = "velocity/mapPercDiff.html"
        self.context['networkId'] = networkId

        return render(request, template, self.context)

class TimeTableMapHandler(View):
    '''  '''
    def __init__(self):
        self.context={}

    def get(self, request, networkId):
        template = 'velocity/table.html'
        self.context['networkId'] = networkId

        return render(request, template, self.context)

class GetRefMapData(View):
    '''This class requests to the database the street secction with travel time '''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        """ streets data """

        networkId = int(request.GET.get('networkId'))
        dayType = request.GET.get('dayType')
        period = request.GET.get('period')

        entity = None
        if networkId ==  741:
            entity = Tramos15MinUOCTReferencia74
        elif networkId == 23491:
            entity = Tramos15MinUOCTReferencia2349
 
        points = entity.objects.filter(tipo_dia=dayType, periodo15=period).order_by('eje', 'tramo', 'dist_en_ruta')

        response = transformData(points)

        return JsonResponse(response, safe=False)


class GetMapData(View):
    '''This class requests to the database the street secction with travel time '''

    def __init__(self):
        """the contructor, context are the parameter given to the html template"""
        self.context={}

    def get(self, request):
        """ streets data """

        networkId = int(request.GET.get('networkId'))

        entity = None
        if networkId == 74:
            entity = Tramos15MinUOCT74
        elif networkId == 2349:
            entity = Tramos15MinUOCT2349
        
        points = entity.objects.filter(visible=1).order_by('eje', 'tramo', 'dist_en_ruta')

        response = transformData(points)

        hour = None
        dayType = None
        if len(points) > 0:
            delta = dt.timedelta(minutes=15)
            upperTimeLimit = (dt.datetime.combine(dt.date.today(), points[0].periodo15) + delta).time()
            hour = "{}-{}".format(points[0].periodo15, upperTimeLimit)
            dayType = points[0].tipo_dia

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

        networkId = int(request.GET.get('networkId'))

        if networkId == 74:
            entity = Tramos15MinUOCT74
        elif networkId == 741:
            entity = Tramos15MinUOCTReferencia74
        elif networkId == 2349:
            entity = Tramos15MinUOCT2349
        elif networkId == 23491:
            entity = Tramos15MinUOCTReferencia2349
   
        points = entity.objects.all().distinct('eje_id', 'tramo', 'calle_origen', 'calle_destino', 'segundos_por_km_tramo')
        
        dataset = []
        for point in points:
            street = {}
            street['corridorId'] = point.eje_id
            street['section'] = point.secuencia_eje_macro
            street['origin'] = point.calle_origen
            street['destination'] = point.calle_destino
            street['metrics'] = point.segundos_por_km_tramo
            street['diff'] = point.diferencia_referencia
            street['refVel'] = point.vel_referencia
            street['nObs'] = point.nobs
            street['grupo'] = point.grupo

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
        obj = Status.objects.get(id='uoct_red74')

        response = {}
        response['status'] = obj.status

        return JsonResponse(response, safe=False)

