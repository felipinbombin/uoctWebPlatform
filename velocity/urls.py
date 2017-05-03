from django.conf.urls import url
from . import views
from velocity.views import PercDiffMapHandler, DiffMapHandler, TimeMapHandler, GetMapData, TimeTableMapHandler, GetTimeTableData, GetDataStatus

urlpatterns = [
	url(r'^timeMap$', TimeMapHandler.as_view(), name='timeMap'),
	url(r'^diffMap$', DiffMapHandler.as_view(), name='diffMap'),
	url(r'^diffPercMap$', PercDiffMapHandler.as_view(), name='diffPercMap'),
	url(r'^getTimeMapData$', GetMapData.as_view()),
	url(r'^getDiffMapData$', GetMapData.as_view()),
        url(r'^timeTable$', TimeTableMapHandler.as_view(), name='timeTable'),
        url(r'^getStreetTableData$', GetTimeTableData.as_view()),
        url(r'^getDataStatus$', GetDataStatus.as_view()),
]
