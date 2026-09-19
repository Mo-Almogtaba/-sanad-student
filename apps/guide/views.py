from django.shortcuts import render
from django.utils import timezone
from .models import (
    GuideSection,
    GuideVideo,
    ImportantDate,
)


# =========================================================
# صفحة الدليل الرئيسية
# =========================================================
def index(request):
    """
    دليل التقديم للجامعات السودانية
    """
    # الأقسام مع كروتها
    sections = GuideSection.objects.filter(
        is_active=True
    ).prefetch_related(
        'cards__items',
        'cards__links',
        'cards__images',
        'cards__videos',
    ).order_by('order')

    # الفيديوهات النشطة
    videos = GuideVideo.objects.filter(
        is_active=True
    ).order_by('order')

    # المواعيد المهمة
    now = timezone.now()
    important_dates = ImportantDate.objects.filter(
        is_active=True,
        date__gte=now,  # فقط القادمة
    ).order_by('date', 'order')[:5]

    # آخر تحديث
    latest_update = None
    latest_section = GuideSection.objects.filter(
        is_active=True
    ).order_by('-created_at').first()
    if latest_section:
        latest_update = latest_section.created_at

    # عدد الأقسام
    total_sections = sections.count()

    context = {
        'sections': sections,
        'videos': videos,
        'important_dates': important_dates,
        'latest_update': latest_update,
        'total_sections': total_sections,
        'page_title': 'دليل التقديم للجامعات السودانية',
    }

    return render(request, 'guide/index.html', context)


# =========================================================
# API: جلب المواعيد المتبقية (للعداد)
# =========================================================
def important_dates_api(request):
    """
    إرجاع المواعيد المهمة كـ JSON
    """
    from django.http import JsonResponse

    now = timezone.now()
    dates = ImportantDate.objects.filter(
        is_active=True,
        date__gte=now,
    ).order_by('date')[:10]

    data = []
    for d in dates:
        delta = d.date - now
        data.append({
            'title': d.title,
            'date': d.date.isoformat(),
            'days': delta.days,
            'hours': delta.seconds // 3600,
            'minutes': (delta.seconds % 3600) // 60,
            'seconds': delta.seconds % 60,
            'is_today': d.is_today,
        })

    return JsonResponse({'dates': data})