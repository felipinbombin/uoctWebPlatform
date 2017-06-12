from django.conf.urls import url
from . import views
from velocity.views import PercDiffMapHandler, DiffMapHandler, TimeMapHandler, GetMapData, TimeTableMapHandler, GetTimeTableData, GetDataStatus, RefMapHandler, GetRefMapData, HistoricalChartHandler

app_name = 'velocity'
urlpatterns = [
	url(r'^timeMap/(?P<networkId>[0-9]+)$', TimeMapHandler.as_view(), name='timeMap'),
	url(r'^diffMap/(?P<networkId>[0-9]+)$', DiffMapHandler.as_view(), name='diffMap'),
	url(r'^diffPercMap/(?P<networkId>[0-9]+)$', PercDiffMapHandler.as_view(), name='diffPercMap'),
	url(r'^refMap/(?P<networkId>[0-9]+)$', RefMapHandler.as_view(), name='refMap'),
        url(r'^getTimeMapData$', GetMapData.as_view(), name='getTimeMapData'),
        url(r'^timeTable/(?P<networkId>[0-9]+)$', TimeTableMapHandler.as_view(), name='timeTable'),
        url(r'^historicalChart/(?P<networkId>[0-9]+)$', HistoricalChartHandler.as_view(), name='historicalChart'),
        url(r'^getStreetTableData$', GetTimeTableData.as_view(), name='getTableData'),
        url(r'^getDataStatus$', GetDataStatus.as_view(), name='getDataStatus'),
        url(r'^getRefMapData$', GetRefMapData.as_view(), name='getRefMapData'),
]
