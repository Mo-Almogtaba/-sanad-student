import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import AccessCode, GuestUsage


# =========================================================
# API: إرسال طلب اشتراك
# =========================================================
@require_POST
def submit_request(request):
    """
    حفظ طلب الاشتراك وإرجاع كود الطلب
    """
    full_name = request.POST.get('full_name', '').strip()
    phone_number = request.POST.get('phone_number', '').strip()

    # التحقق
    if not full_name or not phone_number:
        return JsonResponse({
            'success': False,
            'error': 'الرجاء إدخال جميع البيانات'
        })

    # تنظيف رقم الهاتف
    phone_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
    if not phone_number.startswith('249'):
        phone_number = '249' + phone_number.lstrip('0')

    # هل الرقم موجود مسبقاً؟
    existing = AccessCode.objects.filter(phone_number=phone_number).first()

    if existing:
        if existing.status == 'active' and existing.can_use:
            return JsonResponse({
                'success': False,
                'error': 'لديك كود نشط بالفعل! استخدم /access/activate/ للتفعيل.',
            })
        elif existing.status == 'pending':
            # إرجاع نفس كود الطلب
            wa_text = _build_whatsapp_message(
                existing.full_name, existing.phone_number, existing.request_code
            )
            return JsonResponse({
                'success': True,
                'request_code': existing.request_code,
                'phone_number': existing.phone_number,
                'full_name': existing.full_name,
                'wa_link': f"https://wa.me/{_get_admin_whatsapp()}?text={urllib.parse.quote(wa_text)}",
                'already_exists': True,
            })

    # إنشاء طلب جديد
    access_code = AccessCode.objects.create(
        full_name=full_name,
        phone_number=phone_number,
    )

    # بناء رابط واتساب
    wa_text = _build_whatsapp_message(full_name, phone_number, access_code.request_code)
    wa_link = f"https://wa.me/{_get_admin_whatsapp()}?text={urllib.parse.quote(wa_text)}"

    return JsonResponse({
        'success': True,
        'request_code': access_code.request_code,
        'phone_number': phone_number,
        'full_name': full_name,
        'wa_link': wa_link,
    })


def _get_admin_whatsapp():
    """رقم واتساب المشرف"""
    # يمكن تغييره لاحقاً من SiteSettings
    return '249901958674'


def _build_whatsapp_message(full_name, phone, request_code):
    """بناء نص رسالة واتساب"""
    return f"""السلام عليكم،
طلبت اشتراكاً في منصة سند الطالب:

👤 الاسم: {full_name}
📱 الرقم: {phone}
🎫 كود الطلب: {request_code}

أرجو إنشاء كود الوصول وإرساله لي."""


# =========================================================
# صفحة تفعيل الكود
# =========================================================
def activate(request):
    """
    صفحة تفعيل الكود
    """
    if request.method == 'POST':
        code_input = request.POST.get('code', '').strip().upper()
        phone_input = request.POST.get('phone', '').strip()

        # تنظيف
        phone_input = phone_input.replace('+', '').replace(' ', '').replace('-', '')
        if not phone_input.startswith('249'):
            phone_input = '249' + phone_input.lstrip('0')

        # البحث عن الكود
        try:
            code = AccessCode.objects.get(code__iexact=code_input)
        except AccessCode.DoesNotExist:
            messages.error(request, '❌ الكود غير موجود، تأكد من كتابته بشكل صحيح')
            return render(request, 'access/activate.html')

        # التحقق من الحالة
        if code.status == 'pending':
            messages.error(request, '⏳ الكود قيد المعالجة، تواصل مع الإدارة')
            return render(request, 'access/activate.html')

        if code.status == 'rejected':
            messages.error(request, '❌ تم رفض هذا الطلب')
            return render(request, 'access/activate.html')

        if code.status == 'expired' or code.is_expired:
            messages.error(request, '⏰ انتهت صلاحية الكود')
            return render(request, 'access/activate.html')

        if code.current_uses >= code.max_uses:
            messages.error(request, '⚠️ انتهت المحاولات المسموحة')
            return render(request, 'access/activate.html')

        # التحقق من الرقم
        if code.phone_number != phone_input:
            messages.error(request, '❌ رقم الهاتف غير مطابق للرقم المرتبط بالكود')
            return render(request, 'access/activate.html')

        # ✅ التفعيل
        guest = GuestUsage.get_for_request(request)
        guest.activated_code = code.code
        guest.save()

        messages.success(
            request,
            f'✅ تم التفعيل بنجاح! لديك {code.remaining_uses} محاولة متبقية'
        )
        return redirect('ranks:index')

    return render(request, 'access/activate.html')


# =========================================================
# لوحة تحكم المشرف
# =========================================================
@staff_member_required
def dashboard(request):
    """
    لوحة تحكم المشرف
    """
    pending = AccessCode.objects.filter(status='pending').order_by('created_at')
    active = AccessCode.objects.filter(status='active').order_by('-approved_at')[:50]

    stats = {
        'pending_count': pending.count(),
        'active_count': AccessCode.objects.filter(status='active').count(),
        'total': AccessCode.objects.count(),
    }

    return render(request, 'access/dashboard.html', {
        'pending': pending,
        'active': active,
        'stats': stats,
    })


@staff_member_required
@require_POST
def approve_request(request, pk):
    """
    الموافقة على طلب وإنشاء كود
    """
    access_code = get_object_or_404(AccessCode, pk=pk)

    if access_code.status != 'pending':
        return JsonResponse({'success': False, 'error': 'تم معالجة الطلب مسبقاً'})

    access_code.status = 'active'
    access_code.save()  # سيولّد الكود تلقائياً

    # بناء رابط واتساب للعميل
    wa_text = f"""مرحباً {access_code.full_name}،

تم تفعيل اشتراكك في منصة سند الطالب ✅

🔑 كود الوصول:
{access_code.code}

📊 عدد المحاولات: {access_code.max_uses}
📅 ينتهي في: {access_code.expires_at.strftime('%Y-%m-%d') if access_code.expires_at else 'غير محدد'}

للتفعيل:
1. افتح: /access/activate/
2. أدخل الكود ورقم هاتفك

شكراً لثقتك بنا 🌟"""

    wa_link = f"https://wa.me/{access_code.phone_number}?text={urllib.parse.quote(wa_text)}"

    return JsonResponse({
        'success': True,
        'code': access_code.code,
        'phone_number': access_code.phone_number,
        'wa_link': wa_link,
    })


@staff_member_required
@require_POST
def reject_request(request, pk):
    """
    رفض طلب
    """
    access_code = get_object_or_404(AccessCode, pk=pk)

    if access_code.status != 'pending':
        return JsonResponse({'success': False, 'error': 'تم معالجة الطلب مسبقاً'})

    access_code.status = 'rejected'
    access_code.save()

    return JsonResponse({'success': True})


# =========================================================
# API: حالة الزائر (تُستخدم في ranks)
# =========================================================
def guest_status(request):
    """
    إرجاع حالة الزائر الحالي
    """
    guest = GuestUsage.get_for_request(request)

    return JsonResponse({
        'has_code': bool(guest.activated_code),
        'code': guest.activated_code,
        'remaining_uses': guest.get_code().remaining_uses if guest.get_code() else 0,
        'can_use_free': guest.can_use_free,
        'can_use_any': guest.can_use_any,
        'usage_count': guest.usage_count,
    })