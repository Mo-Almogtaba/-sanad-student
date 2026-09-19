from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


def get_dashboard_stats(user=None):
    """
    إحصائيات لوحة التحكم
    """
    from apps.admission.models import UniversityApplication
    from apps.certificates.models import CertificateRequest
    from apps.contact.models import ContactMessage
    from apps.access.models import AccessCode

    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    return {
        'applications': {
            'total': UniversityApplication.objects.count(),
            'today': UniversityApplication.objects.filter(submitted_at__date=today).count(),
            'week': UniversityApplication.objects.filter(submitted_at__date__gte=week_ago).count(),
            'pending': UniversityApplication.objects.filter(status='pending').count(),
        },
        'certificates': {
            'total': CertificateRequest.objects.count(),
            'today': CertificateRequest.objects.filter(submitted_at__date=today).count(),
            'week': CertificateRequest.objects.filter(submitted_at__date__gte=week_ago).count(),
            'pending': CertificateRequest.objects.filter(status='pending').count(),
        },
        'contact': {
            'total': ContactMessage.objects.count(),
            'today': ContactMessage.objects.filter(submitted_at__date=today).count(),
            'week': ContactMessage.objects.filter(submitted_at__date__gte=week_ago).count(),
            'new': ContactMessage.objects.filter(status='new').count(),
        },
        'access': {
            'total': AccessCode.objects.count(),
            'active': AccessCode.objects.filter(status='active').count(),
            'pending': AccessCode.objects.filter(status='pending').count(),
            'today': AccessCode.objects.filter(created_at__date=today).count(),
        },
    }


def get_recent_items(limit=5):
    """
    آخر العناصر لكل قسم
    """
    from apps.admission.models import UniversityApplication
    from apps.certificates.models import CertificateRequest
    from apps.contact.models import ContactMessage

    return {
        'applications': UniversityApplication.objects.order_by('-submitted_at')[:limit],
        'certificates': CertificateRequest.objects.order_by('-submitted_at')[:limit],
        'contact': ContactMessage.objects.order_by('-submitted_at')[:limit],
    }


def log_activity(user, action, target_type, target_id, details=''):
    """
    تسجيل النشاط
    """
    try:
        from apps.panel.models import ActivityLog
        ActivityLog.objects.create(
            user=user,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
        )
    except Exception as e:
        # تسجيل الخطأ بدون تعطيل العملية
        print(f"⚠️ فشل تسجيل النشاط: {e}")


def filter_applications(request):
    """
    فلترة طلبات التقديم حسب معاملات البحث
    """
    from apps.admission.models import UniversityApplication

    queryset = UniversityApplication.objects.all().order_by('-submitted_at')

    # الحالة
    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)

    # السنة
    year = request.GET.get('year', '')
    if year:
        try:
            queryset = queryset.filter(exam_year=int(year))
        except ValueError:
            pass

    # المساق
    stream = request.GET.get('stream', '')
    if stream:
        queryset = queryset.filter(stream=stream)

    # الولاية
    state = request.GET.get('state', '')
    if state:
        queryset = queryset.filter(state=state)

    # البحث
    search = request.GET.get('q', '')
    if search:
        queryset = queryset.filter(
            Q(application_code__icontains=search) |
            Q(full_name__icontains=search) |
            Q(seat_number__icontains=search) |
            Q(phone_number__icontains=search)
        )

    # الترتيب
    sort = request.GET.get('sort', '-submitted_at')
    if sort in ['submitted_at', '-submitted_at', 'full_name', '-full_name']:
        queryset = queryset.order_by(sort)

    return queryset


def filter_certificates(request):
    """
    فلترة طلبات الشهادات
    """
    from apps.certificates.models import CertificateRequest

    queryset = CertificateRequest.objects.all().order_by('-submitted_at')

    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)

    service = request.GET.get('service', '')
    if service:
        queryset = queryset.filter(service_type=service)

    search = request.GET.get('q', '')
    if search:
        queryset = queryset.filter(
            Q(request_code__icontains=search) |
            Q(full_name__icontains=search) |
            Q(phone_number__icontains=search)
        )

    return queryset


def filter_contact_messages(request):
    """
    فلترة رسائل الاتصال
    """
    from apps.contact.models import ContactMessage

    queryset = ContactMessage.objects.all().order_by('-submitted_at')

    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)

    scope = request.GET.get('scope', '')
    if scope:
        queryset = queryset.filter(scope=scope)

    service = request.GET.get('service', '')
    if service:
        queryset = queryset.filter(service_type=service)

    search = request.GET.get('q', '')
    if search:
        queryset = queryset.filter(
            Q(message_code__icontains=search) |
            Q(full_name__icontains=search) |
            Q(phone_number__icontains=search)
        )

    return queryset


def filter_access_codes(request):
    """
    فلترة أكواد الوصول
    """
    from apps.access.models import AccessCode

    queryset = AccessCode.objects.all().order_by('-created_at')

    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)

    search = request.GET.get('q', '')
    if search:
        queryset = queryset.filter(
            Q(code__icontains=search) |
            Q(request_code__icontains=search) |
            Q(full_name__icontains=search) |
            Q(phone_number__icontains=search)
        )

    return queryset
def filter_announcements(request):
    """
    فلترة الإعلانات
    """
    from apps.config_app.models import Announcement
    from django.db.models import Q

    queryset = Announcement.objects.all().order_by('order', '-created_at')

    status = request.GET.get('status', '')
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)

    search = request.GET.get('q', '')
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    return queryset
def filter_guide_sections(request):
    """
    فلترة أقسام الدليل
    """
    from apps.guide.models import GuideSection
    from django.db.models import Q

    queryset = GuideSection.objects.all().order_by('order', 'created_at')

    status = request.GET.get('status', '')
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)

    search = request.GET.get('q', '')
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    return queryset


def filter_important_dates(request):
    """
    فلترة المواعيد المهمة
    """
    from apps.guide.models import ImportantDate
    from django.db.models import Q

    queryset = ImportantDate.objects.all().order_by('date', 'order')

    status = request.GET.get('status', '')
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)
    elif status == 'upcoming':
        from django.utils import timezone
        queryset = queryset.filter(date__gte=timezone.now())
    elif status == 'past':
        from django.utils import timezone
        queryset = queryset.filter(date__lt=timezone.now())

    return queryset