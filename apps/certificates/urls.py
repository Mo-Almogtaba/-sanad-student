from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('', views.index, name='index'),
    path('request/<str:service_type>/', views.request_form, name='request_form'),
    path('success/<str:code>/', views.success, name='success'),
]