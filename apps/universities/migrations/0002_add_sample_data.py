from django.db import migrations


def create_sample_data(apps, schema_editor):
    """إنشاء بيانات تجريبية للجامعات والكليات"""
    
    University = apps.get_model('universities', 'University')
    Faculty = apps.get_model('universities', 'Faculty')
    AdmissionRequirement = apps.get_model('universities', 'AdmissionRequirement')
    
    # =========================================================
    # جامعة الخرطوم
    # =========================================================
    uok, _ = University.objects.get_or_create(
        name='جامعة الخرطوم',
        defaults={
            'name_en': 'University of Khartoum',
            'slug': 'university-of-khartoum',
            'city': 'الخرطوم',
            'university_type': 'government',
            'established_year': 1902,
            'order': 1,
        }
    )
    
    uok_faculties = [
        {'name': 'كلية الطب', 'category': 'medical', 'years': 6, 'min_2024': 96.1},
        {'name': 'كلية طب الأسنان', 'category': 'medical', 'years': 5, 'min_2024': 94.3},
        {'name': 'كلية الصيدلة', 'category': 'medical', 'years': 5, 'min_2024': 89.6},
        {'name': 'كلية علوم المختبرات الطبية', 'category': 'medical', 'years': 4, 'min_2024': 85.0},
        {'name': 'كلية العلوم الطبية التطبيقية - التمريض', 'category': 'medical', 'years': 4, 'min_2024': 83.9},
        {'name': 'كلية الهندسة - الهندسة المدنية', 'category': 'engineering', 'years': 5, 'min_2024': 86.3},
        {'name': 'كلية الهندسة - الهندسة الكهربائية', 'category': 'engineering', 'years': 5, 'min_2024': 87.7},
        {'name': 'كلية الهندسة - الهندسة الميكانيكية', 'category': 'engineering', 'years': 5, 'min_2024': 86.3},
        {'name': 'كلية العمارة والتخطيط', 'category': 'engineering', 'years': 5, 'min_2024': 84.3},
        {'name': 'كلية الآداب', 'category': 'humanities', 'years': 4, 'min_2024': 70.0},
        {'name': 'كلية القانون', 'category': 'law', 'years': 4, 'min_2024': 85.9},
        {'name': 'كلية العلوم الإدارية', 'category': 'administrative', 'years': 4, 'min_2024': 84.4},
        {'name': 'كلية علوم الحاسوب وتقانة المعلومات - علوم الحاسوب', 'category': 'technology', 'years': 4, 'min_2024': 84.0},
        {'name': 'كلية العلوم - الرياضيات', 'category': 'science', 'years': 4, 'min_2024': 62.9},
        {'name': 'كلية العلوم - الكيمياء', 'category': 'science', 'years': 4, 'min_2024': 71.0},
    ]
    
    for i, fac_data in enumerate(uok_faculties, 1):
        faculty, _ = Faculty.objects.get_or_create(
            name=fac_data['name'],
            university=uok,
            defaults={
                'category': fac_data['category'],
                'duration_years': fac_data['years'],
                'order': i,
                'slug': f"{uok.slug}-{i}",
            }
        )
        
        AdmissionRequirement.objects.get_or_create(
            faculty=faculty,
            year=2024,
            stream='general',
            defaults={
                'min_percentage': fac_data['min_2024'],
                'seats_available': 100,
            }
        )
    
    # =========================================================
    # جامعة النيلين
    # =========================================================
    neelain, _ = University.objects.get_or_create(
        name='جامعة النيلين',
        defaults={
            'name_en': 'Neelain University',
            'slug': 'neelain-university',
            'city': 'الخرطوم',
            'university_type': 'government',
            'established_year': 1956,
            'order': 2,
        }
    )
    
    neelain_faculties = [
        {'name': 'كلية الطب', 'category': 'medical', 'years': 6, 'min_2024': 91.3},
        {'name': 'كلية طب الأسنان', 'category': 'medical', 'years': 5, 'min_2024': 86.7},
        {'name': 'كلية الصيدلة', 'category': 'medical', 'years': 5, 'min_2024': 84.4},
        {'name': 'كلية علوم المختبرات الطبية', 'category': 'medical', 'years': 4, 'min_2024': 80.9},
        {'name': 'كلية علوم التمريض', 'category': 'medical', 'years': 4, 'min_2024': 79.7},
        {'name': 'كلية العلاج الطبيعي', 'category': 'medical', 'years': 4, 'min_2024': 76.4},
        {'name': 'كلية الهندسة - الهندسة المدنية', 'category': 'engineering', 'years': 5, 'min_2024': 74.1},
        {'name': 'كلية الهندسة - الهندسة الكهربائية', 'category': 'engineering', 'years': 5, 'min_2024': 69.6},
        {'name': 'كلية علوم الحاسوب وتقانة المعلومات - علوم الحاسوب', 'category': 'technology', 'years': 4, 'min_2024': 74.4},
        {'name': 'كلية العلوم - الرياضيات', 'category': 'science', 'years': 4, 'min_2024': 60.0},
        {'name': 'كلية الآداب - اللغة العربية', 'category': 'humanities', 'years': 4, 'min_2024': 67.6},
        {'name': 'كلية الآداب - اللغة الإنجليزية', 'category': 'humanities', 'years': 4, 'min_2024': 62.9},
        {'name': 'كلية التجارة - المحاسبة', 'category': 'administrative', 'years': 4, 'min_2024': 72.1},
        {'name': 'كلية القانون', 'category': 'law', 'years': 4, 'min_2024': 74.0},
        {'name': 'كلية الدراسات الاقتصادية والاجتماعية - الاقتصاد', 'category': 'administrative', 'years': 4, 'min_2024': 66.1},
    ]
    
    for i, fac_data in enumerate(neelain_faculties, 1):
        faculty, _ = Faculty.objects.get_or_create(
            name=fac_data['name'],
            university=neelain,
            defaults={
                'category': fac_data['category'],
                'duration_years': fac_data['years'],
                'order': i,
                'slug': f"{neelain.slug}-{i}",
            }
        )
        
        AdmissionRequirement.objects.get_or_create(
            faculty=faculty,
            year=2024,
            stream='general',
            defaults={
                'min_percentage': fac_data['min_2024'],
                'seats_available': 100,
            }
        )
    
    # =========================================================
    # جامعة السودان للعلوم والتكنولوجيا
    # =========================================================
    sust, _ = University.objects.get_or_create(
        name='جامعة السودان للعلوم والتكنولوجيا',
        defaults={
            'name_en': 'Sudan University of Science & Technology',
            'slug': 'sudan-university',
            'city': 'الخرطوم',
            'university_type': 'government',
            'established_year': 1975,
            'order': 3,
        }
    )
    
    sust_faculties = [
        {'name': 'كلية الطب', 'category': 'medical', 'years': 6, 'min_2024': 90.9},
        {'name': 'كلية طب الأسنان', 'category': 'medical', 'years': 5, 'min_2024': 86.6},
        {'name': 'كلية الصيدلة', 'category': 'medical', 'years': 5, 'min_2024': 85.3},
        {'name': 'كلية علوم المختبرات الطبية', 'category': 'medical', 'years': 4, 'min_2024': 81.6},
        {'name': 'كلية الهندسة - الهندسة الميكانيكية', 'category': 'engineering', 'years': 5, 'min_2024': 84.0},
        {'name': 'كلية الهندسة - الهندسة الكهربائية', 'category': 'engineering', 'years': 5, 'min_2024': 77.4},
        {'name': 'كلية الهندسة - الهندسة المدنية', 'category': 'engineering', 'years': 5, 'min_2024': 80.6},
        {'name': 'كلية الهندسة - هندسة الإلكترونيات', 'category': 'engineering', 'years': 5, 'min_2024': 76.7},
        {'name': 'كلية العمارة والتخطيط', 'category': 'engineering', 'years': 5, 'min_2024': 83.0},
        {'name': 'كلية علوم الحاسوب وتقانة المعلومات - هندسة البرمجيات', 'category': 'technology', 'years': 4, 'min_2024': 87.1},
        {'name': 'كلية علوم الحاسوب وتقانة المعلومات - تقانة المعلومات', 'category': 'technology', 'years': 4, 'min_2024': 79.3},
        {'name': 'كلية الدراسات التجارية - المحاسبة والتمويل', 'category': 'administrative', 'years': 4, 'min_2024': 81.7},
        {'name': 'كلية الدراسات التجارية - إدارة الأعمال', 'category': 'administrative', 'years': 4, 'min_2024': 80.3},
        {'name': 'كلية اللغات - اللغة الإنجليزية', 'category': 'humanities', 'years': 4, 'min_2024': 71.9},
        {'name': 'كلية التربية - لغة إنجليزية', 'category': 'education', 'years': 4, 'min_2024': 67.1},
    ]
    
    for i, fac_data in enumerate(sust_faculties, 1):
        faculty, _ = Faculty.objects.get_or_create(
            name=fac_data['name'],
            university=sust,
            defaults={
                'category': fac_data['category'],
                'duration_years': fac_data['years'],
                'order': i,
                'slug': f"{sust.slug}-{i}",
            }
        )
        
        AdmissionRequirement.objects.get_or_create(
            faculty=faculty,
            year=2024,
            stream='general',
            defaults={
                'min_percentage': fac_data['min_2024'],
                'seats_available': 100,
            }
        )


def remove_sample_data(apps, schema_editor):
    """حذف البيانات التجريبية"""
    University = apps.get_model('universities', 'University')
    University.objects.filter(
        name__in=[
            'جامعة الخرطوم',
            'جامعة النيلين',
            'جامعة السودان للعلوم والتكنولوجيا',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, remove_sample_data),
    ]