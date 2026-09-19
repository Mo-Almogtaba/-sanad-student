from django.urls import path
from . import views

app_name = 'admission'

urlpatterns = [
    path('', views.index, name='index'),
    path('success/<str:code>/', views.success, name='success'),
]