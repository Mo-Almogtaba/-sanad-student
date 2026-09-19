from django.urls import path
from . import views

app_name = 'config_app'

urlpatterns = [
    path('', views.index, name='index'),
]