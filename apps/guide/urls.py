from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/dates/', views.important_dates_api, name='dates_api'),
]