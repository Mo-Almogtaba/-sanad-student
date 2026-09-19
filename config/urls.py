"""
الروابط الرئيسية للمشروع
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ===================== الإدارة =====================
    path('admin/', admin.site.urls),
    
    # ===================== المصادقة =====================
    path('accounts/', include('allauth.urls')),
    
    # ===================== التطبيقات =====================
    path('', include('apps.home.urls')),
    path('admission/', include('apps.admission.urls')),
    path('certificates/', include('apps.certificates.urls')),
    path('scholarships/', include('apps.scholarships.urls')),
    path('ranks/', include('apps.ranks.urls')),
    path('contact/', include('apps.contact.urls')),
    path('access/', include('apps.access.urls')), 
    path('panel/', include('apps.panel.urls')),  
    path('guide/', include('apps.guide.urls')),
    path('universities/', include('apps.universities.urls')),
]


# ===================== الملفات الثابتة والوسائط =====================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)