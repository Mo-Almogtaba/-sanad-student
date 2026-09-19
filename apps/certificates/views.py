import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import CertificateRequest


# =========================================================
# الصفحة الرئيسية
# =========================================================
def index(request):
    """
    صفحة الشهادات - عرض الخدمات
    """
    return render(request, 'certificates/index.html')


# =========================================================
# نموذج طلب الشهادة
# =========================================================
def request_form(request, service_type):
    """
    نموذج تقديم طلب شهادة (الأساس / السودانية / الجامعية)
    """
    # التحقق من نوع الخدمة
    VALID_SERVICES = [
        'basic',          # شهادة الأساس
        'high_school',    # الشهادة السودانية
        'university',     # الشهادة الجامعية
    ]

    if service_type not in VALID_SERVICES:
        return redirect('certificates:index')

    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()

            # ✅ بناء رسالة واتساب حسب نوع الخدمة
            if service_type == 'basic':
                # شهادة الأساس
                photo = request.POST.get('photo_available', 'لا')
                national_id = request.POST.get('national_id', '').strip()
                school_name = request.POST.get('school_name', '').strip()
                seat_number = request.POST.get('seat_number', '').strip()
                state = request.POST.get('state', '').strip()
                cert_language = request.POST.get('cert_language', '').strip()

                wa_msg = f"""السلام عليكم،
أرغب في استخراج *شهادة الأساس*.

👤 الاسم: {full_name}
📱 الهاتف: {phone_number}

📋 البيانات:
• صورة فوتوغرافية: {photo}
• إثبات شخصية: {national_id}
• اسم المدرسة: {school_name}
• رقم الجلوس: {seat_number}
• الولاية: {state}
• نوع الشهادة: {cert_language}"""

            elif service_type == 'high_school':
                # الشهادة السودانية
                national_id = request.POST.get('national_id', '').strip()
                seat_number = request.POST.get('seat_number', '').strip()
                school_name = request.POST.get('school_name', '').strip()
                exam_year = request.POST.get('exam_year', '').strip()
                percentage = request.POST.get('percentage', '').strip()
                stream = request.POST.get('stream', '').strip()
                mother_name = request.POST.get('mother_name', '').strip()
                cert_language = request.POST.get('cert_language', '').strip()

                wa_msg = f"""السلام عليكم،
أرغب في استخراج *الشهادة السودانية*.

👤 الاسم: {full_name}
📱 الهاتف: {phone_number}

📋 البيانات:
• إثبات شخصية: {national_id}
• رقم الجلوس: {seat_number}
• اسم المدرسة: {school_name}
• العام: {exam_year}
• النسبة: {percentage}
• المساق: {stream}
• اسم الوالدة: {mother_name}
• لغة الشهادة: {cert_language}"""

            elif service_type == 'university':
                # الشهادة الجامعية
                photo = request.POST.get('photo_available', 'لا')
                university_id = request.POST.get('university_id', '').strip()
                college_major = request.POST.get('college_major', '').strip()
                enroll_date = request.POST.get('enroll_date', '').strip()
                grad_date = request.POST.get('grad_date', '').strip()
                national_id = request.POST.get('national_id', '').strip()
                cert_language = request.POST.get('cert_language', '').strip()

                wa_msg = f"""السلام عليكم،
أرغب في استخراج *الشهادة الجامعية*.

👤 الاسم: {full_name}
📱 الهاتف: {phone_number}

📋 البيانات:
• صورة فوتوغرافية: {photo}
• الرقم الجامعي: {university_id}
• الكلية / التخصص: {college_major}
• تاريخ الدخول: {enroll_date}
• تاريخ التخرج: {grad_date}
• إثبات شخصية: {national_id}
• نوع الشهادة: {cert_language}"""

            # ✅ حفظ في قاعدة البيانات
            cert_request = CertificateRequest.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                service_type=service_type,
                details=wa_msg,
            )

            # ✅ إعادة التوجيه لواتساب
            encoded_msg = urllib.parse.quote(wa_msg)
            whatsapp_number = '249123456789'  # ← غيّر رقمك هنا
            return redirect(f'https://wa.me/{whatsapp_number}?text={encoded_msg}')

        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, f'حدث خطأ: {str(e)}')

    # ✅ عرض النموذج
    context = {
        'service_type': service_type,
    }

    # إضافة بيانات مساعدة للنماذج
    if service_type == 'university':
        from apps.universities.models import University
        context['universities'] = University.objects.filter(is_active=True).order_by('name')

    return render(request, 'certificates/request_form.html', context)


# =========================================================
# صفحة النجاح
# =========================================================
def success(request, code):
    """
    صفحة النجاح
    """
    cert_request = get_object_or_404(CertificateRequest, request_code=code)

    wa_text = f"""السلام عليكم،
طلبت خدمة شهادات في منصة سند الطالب:

🎫 رقم الطلب: {cert_request.request_code}
👤 الاسم: {cert_request.full_name}
📱 الهاتف: {cert_request.phone_number}"""

    encoded = urllib.parse.quote(wa_text)
    wa_link = f"https://wa.me/249123456789?text={encoded}"

    return render(request, 'certificates/success.html', {
        'cert_request': cert_request,
        'wa_link': wa_link,
    })