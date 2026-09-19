from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

from .decorators import (
    panel_login_required,
    section_access_required,
    super_admin_required,
)
from .utils import (
    get_dashboard_stats,
    get_recent_items,
    log_activity,
    filter_applications,
    filter_certificates,
    filter_contact_messages,
    filter_access_codes,
)


# =========================================================
# Auth
# =========================================================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    if not user.profile.is_active:
                        messages.error(request, '❌ حسابك غير مفعّل')
                        logout(request)
                        return render(request, 'panel/login.html')
                except Exception:
                    pass
                messages.success(request, f'✅ مرحباً {user.get_full_name() or user.username}')
                return redirect('panel:dashboard')
            else:
                messages.error(request, '❌ الحساب غير مفعّل')
        else:
            messages.error(request, '❌ اسم المستخدم أو كلمة المرور خطأ')

    return render(request, 'panel/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, '✅ تم تسجيل الخروج بنجاح')
    return redirect('panel:login')


# =========================================================
# Dashboard
# =========================================================
@panel_login_required
def dashboard(request):
    stats = get_dashboard_stats(request.user)
    recent = get_recent_items()

    try:
        accessible_sections = request.user.profile.get_accessible_sections()
    except Exception:
        accessible_sections = []

    context = {
        'stats': stats,
        'recent': recent,
        'accessible_sections': accessible_sections,
        'page_title': 'لوحة التحكم',
    }
    return render(request, 'panel/dashboard.html', context)


# =========================================================
# Applications
# =========================================================
@section_access_required('applications')
def applications(request):
    from apps.admission.models import UniversityApplication
    
    queryset = filter_applications(request)
    
    context = {
        'applications': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'search': request.GET.get('q', ''),
        'year_filter': request.GET.get('year', ''),
        'stream_filter': request.GET.get('stream', ''),
        'state_filter': request.GET.get('state', ''),
        'states': UniversityApplication.STATES,
        'page_title': 'طلبات التقديم الإلكتروني',
    }
    return render(request, 'panel/applications.html', context)


@section_access_required('applications')
def application_detail(request, pk):
    from apps.admission.models import UniversityApplication
    
    application = get_object_or_404(UniversityApplication, pk=pk)
    
    # بناء رابط واتساب للطالب
    wa_number = application.phone_number
    wa_message = f"""مرحباً {application.full_name}،
بخصوص طلبك رقم {application.application_code} في منصة سند الطالب،"""
    
    import urllib.parse
    wa_link = f"https://wa.me/{wa_number}?text={urllib.parse.quote(wa_message)}"
    
    context = {
        'application': application,
        'wa_link': wa_link,
        'page_title': f'طلب {application.application_code}',
    }
    return render(request, 'panel/application_detail.html', context)


@section_access_required('applications')
@require_POST
def application_update_status(request, pk):
    from apps.admission.models import UniversityApplication
    
    application = get_object_or_404(UniversityApplication, pk=pk)
    new_status = request.POST.get('status', '')
    
    valid_statuses = ['pending', 'reviewed', 'accepted', 'rejected']
    if new_status not in valid_statuses:
        return JsonResponse({'success': False, 'error': 'حالة غير صحيحة'})
    
    old_status = application.status
    application.status = new_status
    application.save()
    
    # ✅ تسجيل النشاط
    log_activity(
        user=request.user,
        action='status_change',
        target_type='application',
        target_id=application.pk,
        details=f"تغيير الحالة من {old_status} إلى {new_status}",
    )
    
    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'display': application.get_status_display(),
    })


@section_access_required('applications')
@require_POST
def application_update_notes(request, pk):
    from apps.admission.models import UniversityApplication
    
    application = get_object_or_404(UniversityApplication, pk=pk)
    notes = request.POST.get('notes', '')
    
    application.admin_notes = notes
    application.save()
    
    log_activity(
        user=request.user,
        action='update',
        target_type='application',
        target_id=application.pk,
        details='تحديث ملاحظات الإدارة',
    )
    
    return JsonResponse({'success': True})


# =========================================================
# Certificates
# =========================================================
@section_access_required('certificates')
def certificates(request):
    from apps.certificates.models import CertificateRequest
    
    queryset = filter_certificates(request)
    
    context = {
        'certificates': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'service_filter': request.GET.get('service', ''),
        'search': request.GET.get('q', ''),
        'services': CertificateRequest.SERVICE_CHOICES,
        'page_title': 'طلبات الشهادات',
    }
    return render(request, 'panel/certificates.html', context)


@section_access_required('certificates')
def certificate_detail(request, pk):
    from apps.certificates.models import CertificateRequest
    
    cert = get_object_or_404(CertificateRequest, pk=pk)
    
    import urllib.parse
    wa_message = f"""مرحباً {cert.full_name}،
بخصوص طلبك رقم {cert.request_code} في منصة سند الطالب،"""
    wa_link = f"https://wa.me/{cert.phone_number}?text={urllib.parse.quote(wa_message)}"
    
    context = {
        'certificate': cert,
        'wa_link': wa_link,
        'page_title': f'طلب {cert.request_code}',
    }
    return render(request, 'panel/certificate_detail.html', context)


@section_access_required('certificates')
@require_POST
def certificate_update_status(request, pk):
    from apps.certificates.models import CertificateRequest
    
    cert = get_object_or_404(CertificateRequest, pk=pk)
    new_status = request.POST.get('status', '')
    
    valid = ['pending', 'processing', 'completed', 'cancelled']
    if new_status not in valid:
        return JsonResponse({'success': False, 'error': 'حالة غير صحيحة'})
    
    old_status = cert.status
    cert.status = new_status
    cert.save()
    
    log_activity(
        user=request.user,
        action='status_change',
        target_type='certificate',
        target_id=cert.pk,
        details=f"تغيير الحالة من {old_status} إلى {new_status}",
    )
    
    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'display': cert.get_status_display(),
    })


# =========================================================
# Contact
# =========================================================
@section_access_required('contact')
def contact_messages(request):
    queryset = filter_contact_messages(request)
    
    from apps.contact.models import ContactMessage
    
    context = {
        'messages_list': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'scope_filter': request.GET.get('scope', ''),
        'search': request.GET.get('q', ''),
        'services': ContactMessage.SERVICE_CHOICES,
        'page_title': 'رسائل اتصل بنا',
    }
    return render(request, 'panel/contact.html', context)


@section_access_required('contact')
def contact_detail(request, pk):
    from apps.contact.models import ContactMessage
    
    msg = get_object_or_404(ContactMessage, pk=pk)
    
    # تحديث الحالة تلقائياً إلى "مقروءة"
    if msg.status == 'new':
        msg.status = 'read'
        msg.save()
    
    import urllib.parse
    wa_message = f"""مرحباً {msg.full_name}،
بخصوص رسالتك رقم {msg.message_code} في منصة سند الطالب،"""
    wa_link = f"https://wa.me/{msg.phone_number}?text={urllib.parse.quote(wa_message)}"
    
    context = {
        'message': msg,
        'wa_link': wa_link,
        'page_title': f'رسالة {msg.message_code}',
    }
    return render(request, 'panel/contact_detail.html', context)


@section_access_required('contact')
@require_POST
def contact_update_status(request, pk):
    from apps.contact.models import ContactMessage
    
    msg = get_object_or_404(ContactMessage, pk=pk)
    new_status = request.POST.get('status', '')
    
    valid = ['new', 'read', 'replied', 'archived']
    if new_status not in valid:
        return JsonResponse({'success': False, 'error': 'حالة غير صحيحة'})
    
    msg.status = new_status
    msg.save()
    
    log_activity(
        user=request.user,
        action='status_change',
        target_type='contact',
        target_id=msg.pk,
        details=f"تغيير الحالة إلى {new_status}",
    )
    
    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'display': msg.get_status_display(),
    })


# =========================================================
# Access Codes
# =========================================================
@section_access_required('access')
def access_codes(request):
    queryset = filter_access_codes(request)
    
    context = {
        'access_codes': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'search': request.GET.get('q', ''),
        'page_title': 'أكواد الوصول',
    }
    return render(request, 'panel/access.html', context)


@section_access_required('access')
@require_POST
def access_approve(request, pk):
    from apps.access.models import AccessCode
    
    code = get_object_or_404(AccessCode, pk=pk)
    
    if code.status != 'pending':
        return JsonResponse({'success': False, 'error': 'تم معالجة الطلب مسبقاً'})
    
    code.status = 'active'
    code.save()
    
    log_activity(
        user=request.user,
        action='update',
        target_type='access_code',
        target_id=code.pk,
        details=f'الموافقة على الطلب وإنشاء الكود {code.code}',
    )
    
    return JsonResponse({
        'success': True,
        'code': code.code,
        'phone': code.phone_number,
    })


# =========================================================
# Team Management (Super Admin only)
# =========================================================
@super_admin_required
def team(request):
    """إدارة أعضاء الفريق"""
    from apps.accounts.models import Section, UserProfile
    
    users = User.objects.all().order_by('-date_joined')
    sections = Section.objects.filter(is_active=True)
    
    context = {
        'users': users,
        'sections': sections,
        'page_title': 'إدارة الفريق',
    }
    return render(request, 'panel/team.html', context)


@super_admin_required
@require_POST
def team_create(request):
    """إضافة عضو جديد"""
    from apps.accounts.models import Section, UserProfile
    
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    role = request.POST.get('role', 'staff')
    section_ids = request.POST.getlist('sections')
    
    # التحقق
    if not username or not password:
        return JsonResponse({'success': False, 'error': 'اسم المستخدم وكلمة المرور مطلوبان'})
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'error': 'اسم المستخدم موجود مسبقاً'})
    
    # إنشاء المستخدم
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=full_name,
    )
    user.is_staff = True
    user.save()
    
    # ضبط الصلاحيات
    profile = user.profile
    profile.role = role
    profile.is_active = True
    profile.save()
    
    if role != 'super_admin':
        profile.sections.set(Section.objects.filter(id__in=section_ids))
    
    log_activity(
        user=request.user,
        action='create',
        target_type='user',
        target_id=user.pk,
        details=f'إضافة عضو جديد: {username}',
    )
    
    return JsonResponse({
        'success': True,
        'user_id': user.pk,
        'username': username,
    })


@super_admin_required
@require_POST
def team_update(request, pk):
    """تعديل صلاحيات عضو"""
    from apps.accounts.models import Section
    
    user = get_object_or_404(User, pk=pk)
    role = request.POST.get('role', '')
    section_ids = request.POST.getlist('sections')
    is_active = request.POST.get('is_active') == 'on'
    
    profile = user.profile
    
    if role in ['super_admin', 'team_lead', 'staff']:
        profile.role = role
    
    profile.is_active = is_active
    profile.save()
    
    if role != 'super_admin':
        profile.sections.set(Section.objects.filter(id__in=section_ids))
    else:
        profile.sections.set(Section.objects.all())
    
    log_activity(
        user=request.user,
        action='update',
        target_type='user',
        target_id=user.pk,
        details=f'تحديث صلاحيات: {user.username}',
    )
    
    return JsonResponse({'success': True})


@super_admin_required
@require_POST
def team_toggle(request, pk):
    """تفعيل/تعطيل عضو"""
    user = get_object_or_404(User, pk=pk)
    
    if user == request.user:
        return JsonResponse({'success': False, 'error': 'لا يمكنك تعطيل نفسك'})
    
    profile = user.profile
    profile.is_active = not profile.is_active
    profile.save()
    
    # أيضاً نعطّل حساب المستخدم
    user.is_active = profile.is_active
    user.save()
    
    return JsonResponse({
        'success': True,
        'is_active': profile.is_active,
    })
# =========================================================
# Announcements Management
# =========================================================
@section_access_required('announcements')
def announcements(request):
    """
    إدارة الإعلانات
    """
    from apps.panel.utils import filter_announcements

    queryset = filter_announcements(request)

    context = {
        'announcements': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'search': request.GET.get('q', ''),
        'page_title': 'إدارة الإعلانات',
    }
    return render(request, 'panel/announcements.html', context)


@section_access_required('announcements')
def announcement_add(request):
    """
    إضافة إعلان جديد
    """
    from apps.config_app.models import Announcement

    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            link = request.POST.get('link', '').strip()
            button_text = request.POST.get('button_text', 'اعرف المزيد').strip()
            bg_color = request.POST.get('bg_color', 'linear-gradient(135deg, #1e40af, #3b82f6)').strip()
            order = int(request.POST.get('order', 0) or 0)
            is_active = request.POST.get('is_active') == 'on'
            image = request.FILES.get('image')

            # التحقق
            if not title:
                return JsonResponse({'success': False, 'error': 'العنوان مطلوب'})

            # إنشاء الإعلان
            announcement = Announcement.objects.create(
                title=title,
                description=description,
                link=link,
                button_text=button_text,
                bg_color=bg_color,
                order=order,
                is_active=is_active,
                image=image,
            )

            # تسجيل النشاط
            log_activity(
                user=request.user,
                action='create',
                target_type='announcement',
                target_id=announcement.pk,
                details=f'إضافة إعلان: {title}',
            )

            return JsonResponse({
                'success': True,
                'announcement_id': announcement.pk,
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'طريقة غير مسموحة'})


@section_access_required('announcements')
def announcement_detail(request, pk):
    """
    تفاصيل/تعديل إعلان
    """
    from apps.config_app.models import Announcement

    announcement = get_object_or_404(Announcement, pk=pk)

    context = {
        'announcement': announcement,
        'page_title': f'إعلان: {announcement.title}',
    }
    return render(request, 'panel/announcement_detail.html', context)


@section_access_required('announcements')
@require_POST
def announcement_update(request, pk):
    """
    تحديث إعلان
    """
    from apps.config_app.models import Announcement

    announcement = get_object_or_404(Announcement, pk=pk)

    try:
        announcement.title = request.POST.get('title', announcement.title).strip()
        announcement.description = request.POST.get('description', '').strip()
        announcement.link = request.POST.get('link', '').strip()
        announcement.button_text = request.POST.get('button_text', 'اعرف المزيد').strip()
        announcement.bg_color = request.POST.get('bg_color', announcement.bg_color).strip()
        announcement.order = int(request.POST.get('order', 0) or 0)
        announcement.is_active = request.POST.get('is_active') == 'on'

        # رفع صورة جديدة إن وُجدت
        new_image = request.FILES.get('image')
        if new_image:
            # حذف الصورة القديمة
            if announcement.image:
                try:
                    announcement.image.delete(save=False)
                except Exception:
                    pass
            announcement.image = new_image

        # حذف الصورة إذا طُلب
        if request.POST.get('remove_image') == 'on':
            if announcement.image:
                announcement.image.delete(save=False)
                announcement.image = None

        announcement.save()

        log_activity(
            user=request.user,
            action='update',
            target_type='announcement',
            target_id=announcement.pk,
            details=f'تحديث إعلان: {announcement.title}',
        )

        return JsonResponse({'success': True})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('announcements')
@require_POST
def announcement_toggle(request, pk):
    """
    تفعيل/تعطيل إعلان
    """
    from apps.config_app.models import Announcement

    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.is_active = not announcement.is_active
    announcement.save()

    log_activity(
        user=request.user,
        action='update',
        target_type='announcement',
        target_id=announcement.pk,
        details=f"{'تفعيل' if announcement.is_active else 'تعطيل'} الإعلان",
    )

    return JsonResponse({
        'success': True,
        'is_active': announcement.is_active,
    })


@section_access_required('announcements')
@require_POST
def announcement_delete(request, pk):
    """
    حذف إعلان
    """
    from apps.config_app.models import Announcement

    announcement = get_object_or_404(Announcement, pk=pk)
    title = announcement.title

    # حذف الصورة
    if announcement.image:
        try:
            announcement.image.delete(save=False)
        except Exception:
            pass

    announcement.delete()

    log_activity(
        user=request.user,
        action='delete',
        target_type='announcement',
        target_id=pk,
        details=f'حذف إعلان: {title}',
    )

    return JsonResponse({'success': True})
# =========================================================
# Guide Management
# =========================================================
@section_access_required('guide')
def guide_sections(request):
    """
    إدارة أقسام الدليل
    """
    from apps.guide.models import GuideSection
    from apps.panel.utils import filter_guide_sections

    queryset = filter_guide_sections(request)

    context = {
        'sections': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'search': request.GET.get('q', ''),
        'page_title': 'إدارة دليل التقديم',
    }
    return render(request, 'panel/guide_sections.html', context)


@section_access_required('guide')
@require_POST
def guide_section_create(request):
    """
    إنشاء قسم جديد
    """
    from apps.guide.models import GuideSection

    try:
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', 'fa-info-circle').strip()
        color = request.POST.get('color', '#1e40af').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = request.POST.get('is_active') == 'on'

        if not title:
            return JsonResponse({'success': False, 'error': 'العنوان مطلوب'})

        section = GuideSection.objects.create(
            title=title,
            description=description,
            icon=icon,
            color=color,
            order=order,
            is_active=is_active,
        )

        log_activity(
            user=request.user,
            action='create',
            target_type='application',  # يمكن تغييره لاحقاً
            target_id=section.pk,
            details=f'إنشاء قسم دليل: {title}',
        )

        return JsonResponse({'success': True, 'section_id': section.pk})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
def guide_section_detail(request, pk):
    """
    تفاصيل قسم + إدارة كروته
    """
    from apps.guide.models import GuideSection, GuideCard

    section = get_object_or_404(GuideSection, pk=pk)
    cards = section.cards.all().order_by('order')

    context = {
        'section': section,
        'cards': cards,
        'page_title': f'قسم: {section.title}',
        'card_types': GuideCard.CARD_TYPES,
    }
    return render(request, 'panel/guide_section_detail.html', context)


@section_access_required('guide')
@require_POST
def guide_section_update(request, pk):
    """
    تحديث قسم
    """
    from apps.guide.models import GuideSection

    section = get_object_or_404(GuideSection, pk=pk)

    try:
        section.title = request.POST.get('title', section.title).strip()
        section.description = request.POST.get('description', '').strip()
        section.icon = request.POST.get('icon', section.icon).strip()
        section.color = request.POST.get('color', section.color).strip()
        section.order = int(request.POST.get('order', 0) or 0)
        section.is_active = request.POST.get('is_active') == 'on'
        section.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
@require_POST
def guide_section_toggle(request, pk):
    """
    تفعيل/تعطيل قسم
    """
    from apps.guide.models import GuideSection

    section = get_object_or_404(GuideSection, pk=pk)
    section.is_active = not section.is_active
    section.save()

    return JsonResponse({
        'success': True,
        'is_active': section.is_active,
    })


@section_access_required('guide')
@require_POST
def guide_section_delete(request, pk):
    """
    حذف قسم
    """
    from apps.guide.models import GuideSection

    section = get_object_or_404(GuideSection, pk=pk)
    section.delete()

    return JsonResponse({'success': True})


# ============ Cards ============

@section_access_required('guide')
@require_POST
def guide_card_create(request, section_pk):
    """
    إنشاء كرت جديد
    """
    from apps.guide.models import GuideSection, GuideCard

    section = get_object_or_404(GuideSection, pk=section_pk)

    try:
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        content = request.POST.get('content', '').strip()
        card_type = request.POST.get('card_type', 'accordion')
        icon = request.POST.get('icon', 'fa-circle').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_open_default = request.POST.get('is_open_default') == 'on'
        is_active = request.POST.get('is_active') == 'on'

        if not title:
            return JsonResponse({'success': False, 'error': 'العنوان مطلوب'})

        card = GuideCard.objects.create(
            section=section,
            card_type=card_type,
            title=title,
            subtitle=subtitle,
            content=content,
            icon=icon,
            order=order,
            is_open_default=is_open_default,
            is_active=is_active,
        )

        return JsonResponse({'success': True, 'card_id': card.pk})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
@require_POST
def guide_card_update(request, pk):
    """
    تحديث كرت
    """
    from apps.guide.models import GuideCard

    card = get_object_or_404(GuideCard, pk=pk)

    try:
        card.title = request.POST.get('title', card.title).strip()
        card.subtitle = request.POST.get('subtitle', '').strip()
        card.content = request.POST.get('content', '').strip()
        card.card_type = request.POST.get('card_type', card.card_type)
        card.icon = request.POST.get('icon', card.icon).strip()
        card.order = int(request.POST.get('order', 0) or 0)
        card.is_open_default = request.POST.get('is_open_default') == 'on'
        card.is_active = request.POST.get('is_active') == 'on'
        card.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
@require_POST
def guide_card_toggle(request, pk):
    """
    تفعيل/تعطيل كرت
    """
    from apps.guide.models import GuideCard

    card = get_object_or_404(GuideCard, pk=pk)
    card.is_active = not card.is_active
    card.save()

    return JsonResponse({'success': True, 'is_active': card.is_active})


@section_access_required('guide')
@require_POST
def guide_card_delete(request, pk):
    """
    حذف كرت
    """
    from apps.guide.models import GuideCard

    card = get_object_or_404(GuideCard, pk=pk)
    card.delete()

    return JsonResponse({'success': True})


# ============ Important Dates ============

@section_access_required('guide')
def guide_dates(request):
    """
    إدارة المواعيد المهمة
    """
    from apps.panel.utils import filter_important_dates

    queryset = filter_important_dates(request)

    context = {
        'dates': queryset,
        'total': queryset.count(),
        'status_filter': request.GET.get('status', ''),
        'page_title': 'المواعيد المهمة',
    }
    return render(request, 'panel/guide_dates.html', context)


@section_access_required('guide')
@require_POST
def guide_date_create(request):
    """
    إنشاء موعد جديد
    """
    from apps.guide.models import ImportantDate
    from django.utils.dateparse import parse_datetime

    try:
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date_str = request.POST.get('date', '')
        icon = request.POST.get('icon', 'fa-calendar-alt').strip()
        color = request.POST.get('color', '#dc2626').strip()
        show_countdown = request.POST.get('show_countdown') == 'on'
        order = int(request.POST.get('order', 0) or 0)
        is_active = request.POST.get('is_active') == 'on'

        if not title or not date_str:
            return JsonResponse({'success': False, 'error': 'العنوان والتاريخ مطلوبان'})

        # تحويل التاريخ
        from datetime import datetime
        try:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            return JsonResponse({'success': False, 'error': 'صيغة التاريخ غير صحيحة'})

        important_date = ImportantDate.objects.create(
            title=title,
            description=description,
            date=date,
            icon=icon,
            color=color,
            show_countdown=show_countdown,
            order=order,
            is_active=is_active,
        )

        return JsonResponse({'success': True, 'date_id': important_date.pk})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
@require_POST
def guide_date_update(request, pk):
    """
    تحديث موعد
    """
    from apps.guide.models import ImportantDate
    from datetime import datetime

    important_date = get_object_or_404(ImportantDate, pk=pk)

    try:
        important_date.title = request.POST.get('title', important_date.title).strip()
        important_date.description = request.POST.get('description', '').strip()
        date_str = request.POST.get('date', '')
        if date_str:
            important_date.date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        important_date.icon = request.POST.get('icon', important_date.icon).strip()
        important_date.color = request.POST.get('color', important_date.color).strip()
        important_date.show_countdown = request.POST.get('show_countdown') == 'on'
        important_date.order = int(request.POST.get('order', 0) or 0)
        important_date.is_active = request.POST.get('is_active') == 'on'
        important_date.save()

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
@require_POST
def guide_date_toggle(request, pk):
    """
    تفعيل/تعطيل موعد
    """
    from apps.guide.models import ImportantDate

    important_date = get_object_or_404(ImportantDate, pk=pk)
    important_date.is_active = not important_date.is_active
    important_date.save()

    return JsonResponse({
        'success': True,
        'is_active': important_date.is_active,
    })


@section_access_required('guide')
@require_POST
def guide_date_delete(request, pk):
    """
    حذف موعد
    """
    from apps.guide.models import ImportantDate

    important_date = get_object_or_404(ImportantDate, pk=pk)
    important_date.delete()

    return JsonResponse({'success': True})


# ============ Videos ============

@section_access_required('guide')
def guide_videos(request):
    """
    إدارة الفيديوهات
    """
    from apps.guide.models import GuideVideo

    videos = GuideVideo.objects.all().order_by('order')

    context = {
        'videos': videos,
        'total': videos.count(),
        'page_title': 'الفيديوهات التعليمية',
    }
    return render(request, 'panel/guide_videos.html', context)


@section_access_required('guide')
@require_POST
def guide_video_create(request):
    """
    إنشاء فيديو
    """
    from apps.guide.models import GuideVideo

    try:
        title = request.POST.get('title', '').strip()
        youtube_url = request.POST.get('youtube_url', '').strip()
        description = request.POST.get('description', '').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = request.POST.get('is_active') == 'on'

        if not title or not youtube_url:
            return JsonResponse({'success': False, 'error': 'العنوان والرابط مطلوبان'})

        video = GuideVideo.objects.create(
            title=title,
            youtube_url=youtube_url,
            description=description,
            order=order,
            is_active=is_active,
        )

        return JsonResponse({'success': True, 'video_id': video.pk})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@section_access_required('guide')
@require_POST
def guide_video_delete(request, pk):
    """
    حذف فيديو
    """
    from apps.guide.models import GuideVideo

    video = get_object_or_404(GuideVideo, pk=pk)
    video.delete()

    return JsonResponse({'success': True})
# =========================================================
# Data Entry (Universities Data)
# =========================================================
@section_access_required('data_entry')
def data_entry(request):
    """
    إدارة بيانات الجامعات والكليات والنسب
    """
    from apps.universities.models import University

    universities = University.objects.filter(
        is_active=True
    ).order_by('name')

    context = {
        'universities': universities,
        'page_title': 'إدارة بيانات الجامعات',
    }
    return render(request, 'panel/data_entry.html', context)