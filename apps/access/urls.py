from django.urls import path
from . import views

app_name = 'access'

urlpatterns = [
    # API
    path('submit/', views.submit_request, name='submit_request'),
    path('status/', views.guest_status, name='guest_status'),

    # صفحات
    path('activate/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Actions
    path('approve/<int:pk>/', views.approve_request, name='approve'),
    path('reject/<int:pk>/', views.reject_request, name='reject'),
]