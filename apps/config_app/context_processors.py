from .models import SiteSettings


def site_settings(request):
    """
    إرجاع إعدادات الموقع لكل القوالب
    """
    try:
        settings = SiteSettings.get_settings()
    except Exception:
        settings = None

    return {
        'site_settings': settings,
        'SITE_NAME': settings.site_name if settings else 'سند الطالب',
        'SITE_TAGLINE': settings.site_tagline if settings else 'منصة للمنح والخدمات الأكاديمية',
        'SITE_PHONE': settings.contact_phone if settings else '+249 000 000 000',
        'SITE_EMAIL': settings.contact_email if settings else 'info@sanad-student.com',
        'SITE_ADDRESS': settings.contact_address if settings else 'السودان، أم درمان',
        'SITE_WHATSAPP': settings.whatsapp_number if settings else '249000000000',
        'SITE_ABOUT_US': settings.about_us if settings else '',
        'SITE_FACEBOOK_PAGE': settings.facebook_page if settings else '',
        'SITE_FACEBOOK_GROUP': settings.facebook_group if settings else '',
        'SITE_TELEGRAM_CHANNEL': settings.telegram_channel if settings else '',
        'SITE_TELEGRAM_GROUP': settings.telegram_group if settings else '',
        'SITE_INSTAGRAM': settings.instagram_url if settings else '',
        'SITE_YOUTUBE': settings.youtube_url if settings else '',
        'SITE_TIKTOK': settings.tiktok_url if settings else '',
        'SITE_TWITTER': settings.twitter_url if settings else '',
        'SITE_FACEBOOK': settings.facebook_url if settings else '',
        'SITE_LINKEDIN': settings.linkedin_url if settings else '',
        'DEV_NAME': settings.developer_name if settings else '',
        'DEV_DESCRIPTION': settings.developer_description if settings else '',
        'DEV_EMAIL': settings.developer_email if settings else '',
        'DEV_WHATSAPP': settings.developer_whatsapp if settings else '',
        'DEV_GITHUB': settings.developer_github if settings else '',
        'DEV_WEBSITE': settings.developer_website if settings else '',
                'HERO_BACKGROUND': settings.hero_background.url if settings and settings.hero_background else '',
        'HERO_OVERLAY_OPACITY': settings.hero_overlay_opacity if settings else 0.6,
        'HERO_BTN1_TEXT': settings.hero_btn1_text if settings else 'رتّب رغباتك',
        'HERO_BTN1_ICON': settings.hero_btn1_icon if settings else 'fa-list-ol',
        'HERO_BTN2_TEXT': settings.hero_btn2_text if settings else 'قدّم الآن',
        'HERO_BTN2_ICON': settings.hero_btn2_icon if settings else 'fa-paper-plane',
        'HERO_BADGE': settings.hero_badge if settings else '⭐ منصة سودانية متكاملة للتعليم الجامعي',
        'HERO_TITLE': settings.hero_title if settings else 'بوابتك إلى التقديم الإلكتروني للجامعات والمنح والتوثيق',
        'HERO_DESCRIPTION': settings.hero_description if settings else '',
    }