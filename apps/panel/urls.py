from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Applications
    path('applications/', views.applications, name='applications'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/status/', views.application_update_status, name='application_update_status'),
    path('applications/<int:pk>/notes/', views.application_update_notes, name='application_update_notes'),

    # Certificates
    path('certificates/', views.certificates, name='certificates'),
    path('certificates/<int:pk>/', views.certificate_detail, name='certificate_detail'),
    path('certificates/<int:pk>/status/', views.certificate_update_status, name='certificate_update_status'),

    # Contact
    path('contact/', views.contact_messages, name='contact'),
    path('contact/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('contact/<int:pk>/status/', views.contact_update_status, name='contact_update_status'),

    # Access Codes
    path('access/', views.access_codes, name='access'),
    path('access/<int:pk>/approve/', views.access_approve, name='access_approve'),

    # Team
    path('team/', views.team, name='team'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/<int:pk>/update/', views.team_update, name='team_update'),
    path('team/<int:pk>/toggle/', views.team_toggle, name='team_toggle'),
        # Announcements
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/add/', views.announcement_add, name='announcement_add'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/update/', views.announcement_update, name='announcement_update'),
    path('announcements/<int:pk>/toggle/', views.announcement_toggle, name='announcement_toggle'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
        # Guide Management
    path('guide/', views.guide_sections, name='guide_sections'),
    path('guide/sections/create/', views.guide_section_create, name='guide_section_create'),
    path('guide/sections/<int:pk>/', views.guide_section_detail, name='guide_section_detail'),
    path('guide/sections/<int:pk>/update/', views.guide_section_update, name='guide_section_update'),
    path('guide/sections/<int:pk>/toggle/', views.guide_section_toggle, name='guide_section_toggle'),
    path('guide/sections/<int:pk>/delete/', views.guide_section_delete, name='guide_section_delete'),

    # Cards
    path('guide/sections/<int:section_pk>/cards/create/', views.guide_card_create, name='guide_card_create'),
    path('guide/cards/<int:pk>/update/', views.guide_card_update, name='guide_card_update'),
    path('guide/cards/<int:pk>/toggle/', views.guide_card_toggle, name='guide_card_toggle'),
    path('guide/cards/<int:pk>/delete/', views.guide_card_delete, name='guide_card_delete'),

    # Important Dates
    path('guide/dates/', views.guide_dates, name='guide_dates'),
    path('guide/dates/create/', views.guide_date_create, name='guide_date_create'),
    path('guide/dates/<int:pk>/update/', views.guide_date_update, name='guide_date_update'),
    path('guide/dates/<int:pk>/toggle/', views.guide_date_toggle, name='guide_date_toggle'),
    path('guide/dates/<int:pk>/delete/', views.guide_date_delete, name='guide_date_delete'),

    # Videos
    path('guide/videos/', views.guide_videos, name='guide_videos'),
    path('guide/videos/create/', views.guide_video_create, name='guide_video_create'),
    path('guide/videos/<int:pk>/delete/', views.guide_video_delete, name='guide_video_delete'),
    path('data/', views.data_entry, name='data_entry'),
]