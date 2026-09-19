from django.db import models
from django.shortcuts import render
from django.utils import timezone
from apps.config_app.models import Service, QuickLink, Announcement


def index(request):
    """
    الصفحة الرئيسية
    """
    # الخدمات
    services = Service.objects.filter(is_active=True).order_by('order')

    # الروابط السريعة
    quick_links = QuickLink.objects.filter(is_active=True).order_by('order')

    # الإعلانات المرئية الآن
    now = timezone.now()
    announcements = Announcement.objects.filter(
        is_active=True,
    ).filter(
        # إما لا يوجد starts_at أو بدأ بالفعل
        models.Q(starts_at__isnull=True) | models.Q(starts_at__lte=now)
    ).filter(
        # إما لا يوجد expires_at أو لم ينتهِ بعد
        models.Q(expires_at__isnull=True) | models.Q(expires_at__gte=now)
    ).order_by('order', '-created_at')

    context = {
        'services': services,
        'quick_links': quick_links,
        'announcements': announcements,
    }

    return render(request, 'home/index.html', context)