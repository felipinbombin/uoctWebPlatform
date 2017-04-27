from django.conf.urls import url
from . import views
from velocity.views import DiffMapHandler, GetDiffMapData, TimeMapHandler, GetTimeMapData, TimeTableMapHandler, GetTimeTableData, GetDataStatus

urlpatterns = [
	url(r'^timeMap$', TimeMapHandler.as_view(), name='timeMap'),
	url(r'^getTimeMapData$', GetTimeMapData.as_view()),
	url(r'^diffMap$', DiffMapHandler.as_view(), name='diffMap'),
	url(r'^getDiffMapData$', GetDiffMapData.as_view()),
        url(r'^timeTable$', TimeTableMapHandler.as_view(), name='timeTable'),
        url(r'^getStreetTableData$', GetTimeTableData.as_view()),
        url(r'^getDataStatus$', GetDataStatus.as_view()),
]
