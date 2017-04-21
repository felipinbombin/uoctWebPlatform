from django.conf.urls import url
from . import views
from velocity.views import StreetVelocityMapHandler, GetStreetData, GetPOIData, StreetTimeTableMapHandler, GetStreetTableData

urlpatterns = [
	url(r'^map$', StreetVelocityMapHandler.as_view(), name='map'),
	url(r'^getStreetData$', GetStreetData.as_view()),
	url(r'^getPOIData$', GetPOIData.as_view()),
        url(r'^table$', StreetTimeTableMapHandler.as_view(), name='table'),
        url(r'^getStreetTableData$', GetStreetTableData.as_view()),
]
