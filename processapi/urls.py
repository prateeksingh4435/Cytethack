from django.contrib import admin
from django.urls import path 
from .views import * 

urlpatterns = [

    path('api/process/', ProcessDataAPI.as_view(), name='process_data'),
    path('api/process/<str:hostname>/', HostProcessesAPI.as_view(), name='host_processes'),
    path('monitor', frontend_view, name='frontend_view')

  
]
