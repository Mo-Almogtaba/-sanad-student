from django.db import migrations


def create_default_data(apps, schema_editor):
    """إنشاء البيانات الافتراضية"""
    SiteSettings = apps.get_model('config_app', 'SiteSettings')
    Service = apps.get_model('config_app', 'Service')
    QuickLink = apps.get_model('config_app', 'QuickLink')
    
    # ===================== إعدادات الموقع =====================
    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'توب سينير',
            'site_tagline': 'منصّتي للمنح والخدمات الأكاديمية',
            'hero_badge': '🎓 منصة سودانية متكاملة للتعليم الجامعي',
            'hero_title': 'بوابتك إلى الجامعات والمنح والتوثيق',
            'hero_description': 'نقدّم لك تجربة تعليمية متكاملة تجمع بين التقديم الإلكتروني للجامعات، والتقديم على المنح المحلية والدولية، وترتيب الرغبات، وتوثيق وترجمة الشهادات.',
            'contact_phone': '+249 000 000 000',
            'contact_email': 'info@topsenier.com',
            'contact_address': 'السودان، أم درمان',
            'whatsapp_number': '+249000000000',
        }
    )
    
    # ===================== الخدمات =====================
    services_data = [
        {
            'title': 'التقديم الإلكتروني',
            'description': 'تعرّف على الجامعات، رتّب رغباتك، وقدّم إلكترونياً بخطوات بسيطة.',
            'icon': 'fa-file-signature',
            'url_name': 'admission:index',
            'is_active': True,
            'order': 1,
        },
        {
            'title': 'ترتيب الرغبات',
            'description': 'رتّب رغباتك حسب أولويتك وتوقّع فرص قبولك في الجامعات.',
            'icon': 'fa-list-ol',
            'url_name': 'ranks:index',
            'is_active': True,
            'order': 2,
        },
        {
            'title': 'المنح الدراسية',
            'description': 'اكتشف مجموعة متنوعة من المنح المحلية والدولية الممولة كلياً أو جزئياً.',
            'icon': 'fa-award',
            'url_name': 'scholarships:index',
            'is_active': False,  # ⏸️ معطّل - يظهر "قريباً"
            'order': 3,
        },
        {
            'title': 'الشهادات والتوثيق',
            'description': 'خدمات متكاملة لاستخراج الشهادات، توثيقها، وترجمتها في أسرع وقت.',
            'icon': 'fa-certificate',
            'url_name': 'certificates:index',
            'is_active': True,
            'order': 4,
        },
    ]
    
    for service_data in services_data:
        Service.objects.get_or_create(
            title=service_data['title'],
            defaults=service_data
        )
    
    # ===================== الروابط السريعة =====================
    quick_links_data = [
        {'title': 'دليل القبول', 'url_name': 'admission:index', 'icon': 'fa-book', 'order': 1},
        {'title': 'الجامعات الحكومية', 'url_name': 'admission:index', 'icon': 'fa-landmark', 'order': 2},
        {'title': 'الجامعات الخاصة', 'url_name': 'admission:index', 'icon': 'fa-building', 'order': 3},
        {'title': 'ترتيب الرغبات', 'url_name': 'ranks:index', 'icon': 'fa-list-ol', 'order': 4},
        {'title': 'تواصل معنا', 'url_name': 'contact:index', 'icon': 'fa-envelope', 'order': 5},
    ]
    
    for link_data in quick_links_data:
        QuickLink.objects.get_or_create(
            title=link_data['title'],
            defaults=link_data
        )


def remove_default_data(apps, schema_editor):
    """حذف البيانات الافتراضية عند التراجع"""
    SiteSettings = apps.get_model('config_app', 'SiteSettings')
    Service = apps.get_model('config_app', 'Service')
    QuickLink = apps.get_model('config_app', 'QuickLink')
    
    SiteSettings.objects.all().delete()
    Service.objects.all().delete()
    QuickLink.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('config_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_data, remove_default_data),
    ]