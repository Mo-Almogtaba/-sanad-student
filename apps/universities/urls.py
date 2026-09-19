from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    # APIs
    path('api/university/<int:university_id>/faculties/', 
         views.api_university_faculties, 
         name='api_university_faculties'),

    path('api/save-faculty/', 
         views.api_save_faculty, 
         name='api_save_faculty'),

    path('api/faculty/<int:faculty_id>/delete/', 
         views.api_delete_faculty, 
         name='api_delete_faculty'),

    path('api/create-university/', 
         views.api_create_university, 
         name='api_create_university'),

    path('api/stats/', 
         views.api_stats, 
         name='api_stats'),
]