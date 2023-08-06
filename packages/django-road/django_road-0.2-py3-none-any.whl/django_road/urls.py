from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


# the subdomain can be changed and has to be fetched via api on each request
# the app uuid/id needs to be submitted, too
urlpatterns = [
    path('road-remotedb-api/<str:model_name>/<str:action>/',
        views.RemoteDBAPI.as_view()), # POST without pk
    path('road-remotedb-api/<str:model_name>/<str:action>/<str:pk>/',
        views.RemoteDBAPI.as_view()), # PUT with pk
]

urlpatterns = format_suffix_patterns(urlpatterns)
