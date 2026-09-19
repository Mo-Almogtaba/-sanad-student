from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from apps.panel.decorators import section_access_required
from .models import University, Faculty, AdmissionRequirement


# =========================================================
# API: جلب كليات جامعة معينة
# =========================================================
@section_access_required('data_entry')
def api_university_faculties(request, university_id):
    """
    جلب كليات جامعة معينة مع نسبها
    """
    try:
        university = University.objects.get(pk=university_id)
    except University.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'الجامعة غير موجودة'})

    faculties = Faculty.objects.filter(
        university=university
    ).order_by('id')

    data = []
    for f in faculties:
        # جلب النسبة (2024)
        req = AdmissionRequirement.objects.filter(
            faculty=f,
            year=2024,
        ).first()

        data.append({
            'id': f.id,
            'name': f.name,
            'min_percentage': req.min_percentage if req else None,
            'requirement_id': req.id if req else None,
        })

    return JsonResponse({
        'success': True,
        'university_name': university.name,
        'faculties': data,
    })


# =========================================================
# API: إضافة/تحديث كلية + نسبة
# =========================================================
@section_access_required('data_entry')
@require_POST
def api_save_faculty(request):
    """
    حفظ كلية + نسبتها
    - إذا الكلية موجودة → تحديث النسبة
    - إذا جديدة → إنشاء الكلية + النسبة
    """
    university_id = request.POST.get('university_id', '').strip()
    faculty_name = request.POST.get('faculty_name', '').strip()
    min_percentage = request.POST.get('min_percentage', '').strip()

    # التحقق
    if not university_id:
        return JsonResponse({'success': False, 'error': 'الرجاء اختيار الجامعة'})

    if not faculty_name:
        return JsonResponse({'success': False, 'error': 'الرجاء إدخال اسم الكلية'})

    try:
        min_percentage = float(min_percentage)
        if min_percentage < 0 or min_percentage > 100:
            return JsonResponse({'success': False, 'error': 'النسبة يجب أن تكون بين 0 و 100'})
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'النسبة غير صحيحة'})

    try:
        university = University.objects.get(pk=university_id)
    except University.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'الجامعة غير موجودة'})

    # ✅ التحقق من التكرار
    existing_faculty = Faculty.objects.filter(
        university=university,
        name__iexact=faculty_name,
    ).first()

    is_update = False

    if existing_faculty:
        # الكلية موجودة → تحديث النسبة
        faculty = existing_faculty
        is_update = True

        # البحث عن النسبة
        requirement = AdmissionRequirement.objects.filter(
            faculty=faculty,
            year=2024,
        ).first()

        if requirement:
            requirement.min_percentage = min_percentage
            requirement.save()
        else:
            AdmissionRequirement.objects.create(
                faculty=faculty,
                year=2024,
                stream='general',
                min_percentage=min_percentage,
            )
    else:
        # كلية جديدة
        faculty = Faculty.objects.create(
            university=university,
            name=faculty_name,
            category='other',
            duration_years=4,
            is_active=True,
        )

        # إنشاء النسبة
        AdmissionRequirement.objects.create(
            faculty=faculty,
            year=2024,
            stream='general',
            min_percentage=min_percentage,
        )

    # ✅ تسجيل النشاط
    try:
        from apps.panel.utils import log_activity
        log_activity(
            user=request.user,
            action='update' if is_update else 'create',
            target_type='application',  # مؤقت
            target_id=faculty.pk,
            details=f"{'تحديث' if is_update else 'إضافة'} كلية: {faculty_name} ({min_percentage}%)",
        )
    except Exception:
        pass

    return JsonResponse({
        'success': True,
        'is_update': is_update,
        'faculty_id': faculty.pk,
        'faculty_name': faculty.name,
        'min_percentage': min_percentage,
    })


# =========================================================
# API: حذف كلية
# =========================================================
@section_access_required('data_entry')
@require_POST
def api_delete_faculty(request, faculty_id):
    """
    حذف كلية (مع نسبها)
    """
    try:
        faculty = Faculty.objects.get(pk=faculty_id)
    except Faculty.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'الكلية غير موجودة'})

    name = faculty.name
    faculty.delete()

    # ✅ تسجيل النشاط
    try:
        from apps.panel.utils import log_activity
        log_activity(
            user=request.user,
            action='delete',
            target_type='application',
            target_id=faculty_id,
            details=f'حذف كلية: {name}',
        )
    except Exception:
        pass

    return JsonResponse({'success': True})


# =========================================================
# API: إضافة جامعة جديدة
# =========================================================
@section_access_required('data_entry')
@require_POST
def api_create_university(request):
    """
    إنشاء جامعة جديدة (سريعة)
    """
    name = request.POST.get('name', '').strip()
    university_type = request.POST.get('university_type', 'government')

    if not name:
        return JsonResponse({'success': False, 'error': 'اسم الجامعة مطلوب'})

    # التحقق من التكرار
    if University.objects.filter(name__iexact=name).exists():
        return JsonResponse({'success': False, 'error': 'الجامعة موجودة مسبقاً'})

    university = University.objects.create(
        name=name,
        university_type=university_type,
        is_active=True,
    )

    return JsonResponse({
        'success': True,
        'university_id': university.pk,
        'university_name': university.name,
    })


# =========================================================
# API: إحصائيات
# =========================================================
@section_access_required('data_entry')
def api_stats(request):
    """
    إحصائيات سريعة
    """
    total_universities = University.objects.filter(is_active=True).count()
    total_faculties = Faculty.objects.filter(is_active=True).count()
    total_requirements = AdmissionRequirement.objects.filter(year=2024).count()

    return JsonResponse({
        'success': True,
        'universities': total_universities,
        'faculties': total_faculties,
        'requirements': total_requirements,
    })