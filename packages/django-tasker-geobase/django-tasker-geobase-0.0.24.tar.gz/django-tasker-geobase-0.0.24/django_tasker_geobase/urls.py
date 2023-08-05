from django.urls import path, register_converter
from django_tasker_geobase import views, converters

register_converter(converters.Geobase, 'geobase')

urlpatterns = [
    path('<geobase:geobase>/', views.GeoObject.as_view()),
    path('search/', views.Search.as_view()),
    path('suggestion/', views.Suggestion.as_view()),
]
