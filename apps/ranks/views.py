import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from apps.universities.models import University, Faculty, AdmissionRequirement
from apps.access.models import GuestUsage, AccessCode
from .models import ProbabilityLevel, PredictionSession, PredictionResult


# =========================================================
# الصفحة الرئيسية
# =========================================================
def index(request):
    universities = University.objects.filter(is_active=True)
    probability_levels = ProbabilityLevel.objects.filter(is_active=True)

    context = {
        'universities': universities,
        'probability_levels': probability_levels,
    }
    return render(request, 'ranks/index.html', context)


# =========================================================
# معالجة طلب التوقع
# =========================================================
@require_http_methods(["POST"])
def predict(request):
    try:
        # ✅ التحقق من صلاحية الزائر أولاً
        guest = GuestUsage.get_for_request(request)

        if guest.activated_code:
            # عنده كود مدفوع → تحقق من صلاحيته
            code = guest.get_code()
            if not code or not code.can_use:
                return JsonResponse({
                    'success': False,
                    'error': 'انتهت صلاحية الكود أو المحاولات. تواصل معنا لتجديد الاشتراك.',
                    'show_activation': True,
                })
        else:
            # ما عنده كود → تحقق من المحاولة المجانية
            if not guest.can_use_free:
                return JsonResponse({
                    'success': False,
                    'error': 'انتهت محاولتك المجانية',
                    'show_subscription': True,
                })

        # ✅ قراءة بيانات الطالب
        student_percentage = float(request.POST.get('percentage', 0))
        student_stream = request.POST.get('stream', 'scientific')
        student_name = request.POST.get('student_name', '').strip()

        # ✅ التحقق
        if student_percentage < 0 or student_percentage > 100:
            return JsonResponse({
                'success': False,
                'error': 'النسبة يجب أن تكون بين 0 و 100'
            })

        # ✅ قراءة الرغبات
        faculty_ids = request.POST.getlist('faculties[]')

        if not faculty_ids:
            return JsonResponse({
                'success': False,
                'error': 'لم تختر أي رغبة'
            })

        if len(faculty_ids) > 45:
            return JsonResponse({
                'success': False,
                'error': 'الحد الأقصى 45 رغبة'
            })

        # ✅ إنشاء كود فريد
        session_code = uuid.uuid4().hex[:12]

        # ✅ إنشاء الجلسة
        session = PredictionSession.objects.create(
            student_name=student_name or 'طالب',
            student_percentage=student_percentage,
            student_stream=student_stream,
            session_code=session_code,
        )

        # ✅ جلب الكليات
        faculties = Faculty.objects.filter(
            id__in=faculty_ids,
            is_active=True
        ).select_related('university')

        faculty_dict = {f.id: f for f in faculties}
        ordered_faculties = [
            faculty_dict[int(fid)]
            for fid in faculty_ids
            if int(fid) in faculty_dict
        ]

        # ✅ مستويات الاحتمالية
        probability_levels = list(ProbabilityLevel.objects.filter(is_active=True))

        # ✅ معالجة كل رغبة
        for priority, faculty in enumerate(ordered_faculties, 1):
            requirement = AdmissionRequirement.objects.filter(
                faculty=faculty,
                year=2024,
            ).first()

            if not requirement:
                continue

            min_percentage = requirement.min_percentage
            difference = student_percentage - min_percentage

            # ✅ تحديد مستوى الاحتمالية
            probability_level = None
            for level in probability_levels:
                try:
                    if level.matches_difference(difference):
                        probability_level = level
                        break
                except AttributeError:
                    # fallback إذا لم توجد الدالة
                    if (hasattr(level, 'min_difference') and
                            hasattr(level, 'max_difference') and
                            level.min_difference <= difference < level.max_difference):
                        probability_level = level
                        break

            PredictionResult.objects.create(
                session=session,
                faculty=faculty,
                priority=priority,
                student_percentage=student_percentage,
                min_percentage=min_percentage,
                difference=difference,
                probability_level=probability_level,
            )

        # ✅ تسجيل الاستخدام (بعد نجاح التوقع)
        guest.use()

        # ✅ إعادة التوجيه
        return JsonResponse({
            'success': True,
            'session_code': session_code,
            'redirect_url': f'/ranks/results/?code={session_code}',
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'حدث خطأ: {str(e)}'
        })


# =========================================================
# صفحة النتائج
# =========================================================
def results(request):
    session_code = request.GET.get('code')

    if not session_code:
        return redirect('ranks:index')

    try:
        session = PredictionSession.objects.get(session_code=session_code)
    except PredictionSession.DoesNotExist:
        return redirect('ranks:index')

    results_qs = session.results.all().select_related(
        'faculty',
        'faculty__university',
        'probability_level',
    ).order_by('priority')

    # ✅ إحصائيات آمنة (تتحقق من وجود slug)
    def count_by_slug(slug):
        try:
            return results_qs.filter(probability_level__slug=slug).count()
        except Exception:
            return 0

    stats = {
        'total': results_qs.count(),
        'very_high': count_by_slug('very-high'),
        'high': count_by_slug('high'),
        'good': count_by_slug('good'),
        'medium': count_by_slug('medium'),
        'low': count_by_slug('low'),
        'very_low': count_by_slug('very-low'),
        'zero': count_by_slug('zero'),
    }

    context = {
        'session': session,
        'results': results_qs,
        'stats': stats,
    }
    return render(request, 'ranks/results.html', context)


# =========================================================
# APIs
# =========================================================
def api_search_faculties(request):
    query = request.GET.get('q', '').strip()
    university_id = request.GET.get('university', '')
    category = request.GET.get('category', '')

    faculties = Faculty.objects.filter(
        is_active=True
    ).select_related('university')

    if query:
        q_filter = Q(name__icontains=query) | Q(university__name__icontains=query)
        try:
            Faculty._meta.get_field('name_en')
            q_filter |= Q(name_en__icontains=query)
        except Exception:
            pass
        faculties = faculties.filter(q_filter)

    if university_id:
        faculties = faculties.filter(university_id=university_id)

    if category:
        try:
            Faculty._meta.get_field('category')
            faculties = faculties.filter(category=category)
        except Exception:
            pass

    faculties = faculties.order_by('university__name', 'name')[:50]

    data = []
    for f in faculties:
        requirement = AdmissionRequirement.objects.filter(
            faculty=f,
            year=2024,
        ).first()

        category_display = ''
        try:
            category_display = f.get_category_display()
        except Exception:
            category_display = ''

        duration_years = getattr(f, 'duration_years', None)

        data.append({
            'id': f.id,
            'name': f.name,
            'university': f.university.name,
            'category': category_display,
            'min_percentage': requirement.min_percentage if requirement else None,
        })

    return JsonResponse({'success': True, 'faculties': data})


def api_faculties_by_university(request):
    university_id = request.GET.get('university_id', '')

    if not university_id:
        return JsonResponse({'success': False, 'error': 'لم يتم تحديد الجامعة'})

    faculties = Faculty.objects.filter(
        university_id=university_id,
        is_active=True,
    ).order_by('name')

    data = []
    for f in faculties:
        requirement = AdmissionRequirement.objects.filter(
            faculty=f,
            year=2024,
        ).first()

        data.append({
            'id': f.id,
            'name': f.name,
            'min_percentage': requirement.min_percentage if requirement else None,
        })

    return JsonResponse({'success': True, 'faculties': data})