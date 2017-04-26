from django.conf.urls import url
from . import views
from velocity.views import StreetVelocityDiffMapHandler, GetStreetDiffData, StreetVelocityMapHandler, GetStreetData, StreetTimeTableMapHandler, GetStreetTableData

urlpatterns = [
	url(r'^timeMap$', StreetVelocityMapHandler.as_view(), name='timeMap'),
	url(r'^getStreetData$', GetStreetData.as_view()),
	url(r'^diffMap$', StreetVelocityDiffMapHandler.as_view(), name='diffMap'),
	url(r'^getStreetDiffData$', GetStreetDiffData.as_view()),
        url(r'^timeTable$', StreetTimeTableMapHandler.as_view(), name='timeTable'),
        url(r'^getStreetTableData$', GetStreetTableData.as_view()),
]
