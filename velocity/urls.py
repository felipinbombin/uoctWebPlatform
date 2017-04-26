from django.conf.urls import url
from . import views
from velocity.views import StreetVelocityDiffMapHandler, GetStreetDiffData, StreetVelocityMapHandler, GetStreetData, StreetTimeTableMapHandler, GetStreetTableData

urlpatterns = [
	url(r'^map$', StreetVelocityMapHandler.as_view(), name='map'),
	url(r'^getStreetData$', GetStreetData.as_view()),
	url(r'^mapDiff$', StreetVelocityDiffMapHandler.as_view(), name='mapDiff'),
	url(r'^getStreetDiffData$', GetStreetDiffData.as_view()),
        url(r'^table$', StreetTimeTableMapHandler.as_view(), name='table'),
        url(r'^getStreetTableData$', GetStreetTableData.as_view()),
]
