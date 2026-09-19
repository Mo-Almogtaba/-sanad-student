from django.db import migrations


def create_default_levels(apps, schema_editor):
    """إنشاء مستويات الاحتمالية الافتراضية"""
    ProbabilityLevel = apps.get_model('ranks', 'ProbabilityLevel')
    
    levels = [
        {
            'name': 'عالية جداً',
            'slug': 'very-high',
            'min_difference': 10,
            'max_difference': None,
            'color': '#28a745',
            'icon': 'bi-check-circle-fill',
            'order': 1,
        },
        {
            'name': 'عالية',
            'slug': 'high',
            'min_difference': 5,
            'max_difference': 10,
            'color': '#5cb85c',
            'icon': 'bi-check-circle',
            'order': 2,
        },
        {
            'name': 'جيدة',
            'slug': 'good',
            'min_difference': 0,
            'max_difference': 5,
            'color': '#ffc107',
            'icon': 'bi-emoji-smile',
            'order': 3,
        },
        {
            'name': 'ضعيفة',
            'slug': 'low',
            'min_difference': -3,
            'max_difference': 0,
            'color': '#fd7e14',
            'icon': 'bi-emoji-neutral',
            'order': 4,
        },
        {
            'name': 'ضعيفة جداً',
            'slug': 'very-low',
            'min_difference': -7,
            'max_difference': -3,
            'color': '#dc3545',
            'icon': 'bi-emoji-frown',
            'order': 5,
        },
        {
            'name': 'منعدمة',
            'slug': 'zero',
            'min_difference': -100,
            'max_difference': -7,
            'color': '#6c757d',
            'icon': 'bi-x-circle',
            'order': 6,
        },
    ]
    
    for level_data in levels:
        ProbabilityLevel.objects.get_or_create(
            slug=level_data['slug'],
            defaults=level_data
        )


def remove_default_levels(apps, schema_editor):
    """حذف مستويات الاحتمالية عند التراجع"""
    ProbabilityLevel = apps.get_model('ranks', 'ProbabilityLevel')
    ProbabilityLevel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ranks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_levels, remove_default_levels),
    ]