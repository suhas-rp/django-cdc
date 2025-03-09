from django.urls import path
from . import views

urlpatterns = [
    path("api/statistics/",views.statistics.as_view(),name="statistics-generator")
]
