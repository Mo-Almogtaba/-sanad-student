"""
Context Processor - يوفر إعدادات الموقع لكل القوالب
"""


def site_settings(request):
    """
    إرجاع إعدادات الموقع لكل القوالب
    """
    # هذه القيم ستُستبدل بقيم من قاعدة البيانات لاحقاً
    return {
        'SITE_NAME': 'توب سينير',
        'SITE_TAGLINE': 'منصّتي للمنح والخدمات الأكاديمية',
        'SITE_PHONE': '+249 000 000 000',
        'SITE_EMAIL': 'info@topsenier.com',
        'SITE_ADDRESS': 'السودان، أم درمان',
        'SITE_WHATSAPP': '+249000000000',
    }