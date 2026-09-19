from django.shortcuts import render
from apps.config_app.models import Service, QuickLink


def index(request):
    """
    الصفحة الرئيسية
    """
    # ✅ جلب الخدمات النشطة
    services = Service.objects.filter(is_active=True)
    
    # ✅ جلب الروابط السريعة النشطة
    quick_links = QuickLink.objects.filter(is_active=True)
    
    context = {
        'services': services,
        'quick_links': quick_links,
    }
    
    return render(request, 'home/index.html', context)