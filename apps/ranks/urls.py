from django.urls import path
from . import views

app_name = 'ranks'

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('results/', views.results, name='results'),
    path('api/search-faculties/', views.api_search_faculties, name='api_search_faculties'),
    path('api/faculties-by-university/', views.api_faculties_by_university, name='api_faculties_by_university'),
]