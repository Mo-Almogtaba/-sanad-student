from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Service, QuickLink, Announcement


# =========================================================
# إدارة إعدادات الموقع
# =========================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    إدارة إعدادات الموقع
    """

    fieldsets = (
        ('معلومات الموقع', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Hero Section', {
            'fields': (
                'hero_badge', 'hero_title', 'hero_description',
                'hero_background', 'hero_overlay_opacity',
                'hero_btn1_text', 'hero_btn1_icon',
                'hero_btn2_text', 'hero_btn2_icon',
            )
        }),
        ('من نحن', {
            'fields': ('about_us',)
        }),
        ('معلومات التواصل', {
            'fields': ('contact_phone', 'contact_email', 'contact_address', 'whatsapp_number')
        }),
        ('روابط التواصل الاجتماعي', {
            'fields': (
                'facebook_page', 'facebook_group',
                'telegram_channel', 'telegram_group',
                'instagram_url', 'youtube_url',
                'tiktok_url', 'twitter_url',
                'facebook_url', 'linkedin_url',
            ),
            'classes': ('collapse',)
        }),
        ('معلومات المطور', {
            'fields': (
                'developer_name', 'developer_description',
                'developer_email', 'developer_whatsapp',
                'developer_github', 'developer_website',
            ),
            'classes': ('collapse',)
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
    )

    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        """منع إضافة أكثر من إعدادات واحدة"""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """منع حذف الإعدادات"""
        return False


# =========================================================
# إدارة الخدمات
# =========================================================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    إدارة الخدمات (الكروت)
    """

    list_display = ('title', 'icon', 'url_name', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description')

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'description', 'icon')
        }),
        ('الربط', {
            'fields': ('url_name',)
        }),
        ('الحالة والترتيب', {
            'fields': ('is_active', 'order')
        }),
    )


# =========================================================
# إدارة الروابط السريعة
# =========================================================
@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    """
    إدارة الروابط السريعة
    """

    list_display = ('title', 'icon', 'url_name', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    search_fields = ('title',)


# =========================================================
# إدارة الإعلانات (البانر المتحرك)
# =========================================================
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """
    إدارة الإعلانات في البانر المتحرك
    """

    list_display = ['preview_image', 'title', 'is_active', 'order', 'get_period', 'created_at']
    list_editable = ['is_active', 'order']
    list_display_links = ['title']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'image_preview']

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'description')
        }),
        ('الصورة', {
            'fields': ('image', 'image_preview')
        }),
        ('الرابط والزر', {
            'fields': ('link', 'button_text')
        }),
        ('التصميم', {
            'fields': ('bg_color',)
        }),
        ('الحالة والترتيب', {
            'fields': ('is_active', 'order')
        }),
        ('فترة العرض', {
            'fields': ('starts_at', 'expires_at'),
            'classes': ('collapse',),
            'description': 'اتركهما فارغين للعرض الدائم'
        }),
    )

    @admin.display(description='معاينة')
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:100px; height:40px; object-fit:cover; border-radius:5px;" />',
                obj.image.url
            )
        return '—'

    @admin.display(description='معاينة الصورة')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:600px; border-radius:10px; margin-top:10px;" />',
                obj.image.url
            )
        return 'لم يتم رفع صورة بعد'

    @admin.display(description='فترة العرض')
    def get_period(self, obj):
        if not obj.starts_at and not obj.expires_at:
            return 'دائم'
        parts = []
        if obj.starts_at:
            parts.append(f"من {obj.starts_at.strftime('%Y-%m-%d')}")
        if obj.expires_at:
            parts.append(f"إلى {obj.expires_at.strftime('%Y-%m-%d')}")
        return ' '.join(parts)