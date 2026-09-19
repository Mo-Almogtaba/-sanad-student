import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import UniversityApplication


# =========================================================
# سنوات الامتحان المتاحة
# =========================================================
EXAM_YEARS = [2026, 2025, 2024, 2023, 2022, 2021, 2020]


# =========================================================
# الصفحة الرئيسية - نموذج التقديم
# ✅ متاح للجميع بدون كود access
# =========================================================
def index(request):
    """
    نموذج التقديم الإلكتروني - مجاني للجميع
    """
    if request.method == 'POST':
        try:
            # قراءة البيانات
            full_name = request.POST.get('full_name', '').strip()
            seat_number = request.POST.get('seat_number', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            state = request.POST.get('state', '')
            exam_year = request.POST.get('exam_year', '')
            stream = request.POST.get('stream', 'scientific')
            optional_subject = request.POST.get('optional_subject', '').strip()
            application_type = request.POST.get('application_type', 'bachelor')
            failed_subjects = request.POST.get('failed_subjects', '').strip()
            preferences_file = request.FILES.get('preferences_file')

            # ✅ التحقق
            errors = []

            if not full_name or len(full_name.split()) < 3:
                errors.append('الاسم يجب أن يكون رباعياً على الأقل')

            if not seat_number:
                errors.append('رقم الجلوس مطلوب')

            if not phone_number:
                errors.append('رقم الهاتف مطلوب')

            if not state:
                errors.append('الولاية مطلوبة')

            if not exam_year:
                errors.append('سنة الامتحان مطلوبة')

            if not optional_subject:
                errors.append('المادة الاختيارية مطلوبة')

            if not preferences_file:
                errors.append('ملف ترتيب الرغبات مطلوب')

            if application_type == 'diploma' and not failed_subjects:
                errors.append('المواد الراسب بها مطلوبة للتقديم للدبلوم')

            # التحقق من حجم الملف
            if preferences_file and preferences_file.size > 5 * 1024 * 1024:
                errors.append('حجم الملف يجب ألا يتجاوز 5 ميجابايت')

            # التحقق من نوع الملف
            if preferences_file:
                allowed_ext = ['jpg', 'jpeg', 'png', 'pdf']
                ext = preferences_file.name.split('.')[-1].lower()
                if ext not in allowed_ext:
                    errors.append('صيغة الملف يجب أن تكون صورة أو PDF')

            if errors:
                return render(request, 'admission/index.html', {
                    'errors': errors,
                    'STATES': UniversityApplication.STATES,
                    'EXAM_YEARS': EXAM_YEARS,
                    'form_data': request.POST,
                })

            # ✅ التحقق من عدم التكرار
            existing = UniversityApplication.objects.filter(
                seat_number=seat_number,
                exam_year=exam_year,
            ).first()

            if existing:
                return render(request, 'admission/index.html', {
                    'errors': [
                        f'⚠️ لقد قدمت طلباً مسبقاً بنفس رقم الجلوس. رقم طلبك: {existing.application_code}'
                    ],
                    'STATES': UniversityApplication.STATES,
                    'EXAM_YEARS': EXAM_YEARS,
                    'existing_app': existing,
                })

            # ✅ حفظ الطلب
            application = UniversityApplication.objects.create(
                full_name=full_name,
                seat_number=seat_number,
                phone_number=phone_number,
                state=state,
                exam_year=exam_year,
                stream=stream,
                optional_subject=optional_subject,
                application_type=application_type,
                failed_subjects=failed_subjects if application_type == 'diploma' else '',
                preferences_file=preferences_file,
            )

            messages.success(
                request,
                f'✅ تم استلام طلبك بنجاح! رقم الطلب: {application.application_code}'
            )
            return redirect('admission:success', code=application.application_code)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return render(request, 'admission/index.html', {
                'errors': [f'حدث خطأ: {str(e)}'],
                'STATES': UniversityApplication.STATES,
                'EXAM_YEARS': EXAM_YEARS,
                'form_data': request.POST,
            })

    return render(request, 'admission/index.html', {
        'STATES': UniversityApplication.STATES,
        'EXAM_YEARS': EXAM_YEARS,
    })


# =========================================================
# صفحة النجاح
# =========================================================
def success(request, code):
    """
    صفحة النجاح بعد التقديم
    """
    application = get_object_or_404(UniversityApplication, application_code=code)

    # بناء رسالة واتساب (لك أنت)
    wa_text = f"""السلام عليكم،
قدمت طلباً إلكترونياً في منصة سند الطالب:

🎫 رقم الطلب: {application.application_code}
👤 الاسم: {application.full_name}
🎫 رقم الجلوس: {application.seat_number}
📱 رقم الهاتف: {application.phone_number}
🏛️ الولاية: {application.state_display}
📅 سنة الامتحان: {application.exam_year}
📚 المساق: {application.stream_display}
📝 المادة الاختيارية: {application.optional_subject}
🎓 نوع التقديم: {application.type_display}"""

    if application.failed_subjects:
        wa_text += f"\n❌ المواد الراسب بها: {application.failed_subjects}"

    wa_text += "\n\nأرجو تأكيد طلبي ومتابعته. شكراً 🌟"

    encoded = urllib.parse.quote(wa_text)
    wa_link = f"https://wa.me/249123456789?text={encoded}"  # ← غيّر الرقم

    return render(request, 'admission/success.html', {
        'application': application,
        'wa_link': wa_link,
    })