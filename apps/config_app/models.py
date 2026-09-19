from django.db import models


class SiteSettings(models.Model):
    """
    إعدادات الموقع العامة
    (يمكن تعديلها من لوحة الإدارة)
    """
    
    # ===================== معلومات الموقع =====================
    site_name = models.CharField(
        max_length=100,
        default='توب سينير',
        verbose_name='اسم الموقع'
    )
    
    site_tagline = models.CharField(
        max_length=200,
        default='منصّتي للمنح والخدمات الأكاديمية',
        verbose_name='الشعار الفرعي'
    )
    
    # ===================== Hero Section =====================
    hero_badge = models.CharField(
        max_length=200,
        default='🎓 منصة سودانية متكاملة للتعليم الجامعي',
        verbose_name='شعار Hero'
    )
    
    hero_title = models.CharField(
        max_length=300,
        default='بوابتك إلى الجامعات والمنح والتوثيق',
        verbose_name='عنوان Hero'
    )
    
    hero_description = models.TextField(
        default='نقدّم لك تجربة تعليمية متكاملة تجمع بين التقديم الإلكتروني، والمنح، وترتيب الرغبات، وتوثيق الشهادات.',
        verbose_name='وصف Hero'
    )
    # ===================== Hero Background =====================
    hero_background = models.ImageField(
        upload_to='hero/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='خلفية Hero',
        help_text='المقاس المثالي: 1920×1080 بكسل - حجم أقل من 1 ميجا'
    )

    hero_overlay_opacity = models.FloatField(
        default=0.6,
        verbose_name='شفافية الطبقة الداكنة',
        help_text='من 0 (بدون طبقة) إلى 1 (طبقة معتمة تماماً)'
    )

    # ===================== نصوص الأزرار =====================
    hero_btn1_text = models.CharField(
        max_length=50,
        default='رتّب رغباتك',
        verbose_name='نص الزر الأول',
        blank=True,
    )
    hero_btn1_icon = models.CharField(
        max_length=50,
        default='fa-list-ol',
        verbose_name='أيقونة الزر الأول',
        blank=True,
        help_text='مثال: fa-list-ol',
    )

    hero_btn2_text = models.CharField(
        max_length=50,
        default='قدّم الآن',
        verbose_name='نص الزر الثاني',
        blank=True,
    )
    hero_btn2_icon = models.CharField(
        max_length=50,
        default='fa-paper-plane',
        verbose_name='أيقونة الزر الثاني',
        blank=True,
    )
    
    # ===================== معلومات التواصل =====================
    contact_phone = models.CharField(
        max_length=50,
        default='+249 000 000 000',
        verbose_name='رقم الهاتف'
    )
    
    contact_email = models.EmailField(
        default='info@topsenier.com',
        verbose_name='البريد الإلكتروني'
    )
    
    contact_address = models.CharField(
        max_length=200,
        default='السودان، أم درمان',
        verbose_name='العنوان'
    )
    
    whatsapp_number = models.CharField(
        max_length=50,
        default='+249000000000',
        verbose_name='رقم الواتساب'
    )
    
    # ===================== روابط التواصل الاجتماعي =====================
    facebook_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='رابط فيسبوك'
    )
    
    linkedin_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='رابط لينكدإن'
    )
        # ===================== من نحن =====================
    about_us = models.TextField(
        default='منصة سودانية متكاملة تهدف إلى تسهيل رحلة الطالب الأكاديمية من التقديم للجامعات حتى استخراج الشهادات.',
        verbose_name='من نحن',
    )
    
    # ===================== روابط التواصل الاجتماعي =====================
    facebook_page = models.URLField(
        blank=True, null=True,
        verbose_name='صفحة فيسبوك',
    )
    facebook_group = models.URLField(
        blank=True, null=True,
        verbose_name='مجموعة فيسبوك',
    )
    telegram_channel = models.URLField(
        blank=True, null=True,
        verbose_name='قناة تيليجرام',
    )
    telegram_group = models.URLField(
        blank=True, null=True,
        verbose_name='مجموعة تيليجرام',
    )
    instagram_url = models.URLField(
        blank=True, null=True,
        verbose_name='إنستغرام',
    )
    youtube_url = models.URLField(
        blank=True, null=True,
        verbose_name='يوتيوب',
    )
    tiktok_url = models.URLField(
        blank=True, null=True,
        verbose_name='تيك توك',
    )
    twitter_url = models.URLField(
        blank=True, null=True,
        verbose_name='X (تويتر)',
    )
    
    # ===================== معلومات المطور =====================
    developer_name = models.CharField(
        max_length=100,
        default='',
        blank=True,
        verbose_name='اسم المطور',
    )
    developer_description = models.TextField(
        default='',
        blank=True,
        verbose_name='وصف المطور',
    )
    developer_email = models.EmailField(
        default='',
        blank=True,
        verbose_name='بريد المطور',
    )
    developer_whatsapp = models.CharField(
        max_length=50,
        default='',
        blank=True,
        verbose_name='واتساب المطور',
    )
    developer_github = models.URLField(
        default='',
        blank=True,
        verbose_name='GitHub المطور',
    )
    developer_website = models.URLField(
        default='',
        blank=True,
        verbose_name='موقع المطور',
    )
    
    # ===================== الحالة =====================
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخر تحديث'
    )
    
    class Meta:
        verbose_name = 'إعدادات الموقع'
        verbose_name_plural = 'إعدادات الموقع'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        """التأكد من وجود إعدادات واحدة فقط"""
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('لا يمكن إنشاء أكثر من إعدادات واحدة للموقع')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """الحصول على الإعدادات (أو إنشاؤها إذا لم توجد)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class Service(models.Model):
    """
    الخدمات (الكروت في الصفحة الرئيسية)
    يمكن تفعيلها/تعطيلها من لوحة الإدارة
    """
    
    ICON_CHOICES = [
        ('fa-file-signature', '📝 التقديم الإلكتروني'),
        ('fa-list-ol', '🎯 ترتيب الرغبات'),
        ('fa-award', '🏆 المنح الدراسية'),
        ('fa-certificate', '📜 الشهادات والتوثيق'),
        ('fa-graduation-cap', '🎓 الجامعات'),
        ('fa-book', '📚 الكورسات'),
        ('fa-envelope', '📧 اتصل بنا'),
    ]
    
    # ===================== المعلومات =====================
    title = models.CharField(
        max_length=100,
        verbose_name='العنوان'
    )
    
    description = models.TextField(
        verbose_name='الوصف'
    )
    
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        default='fa-graduation-cap',
        verbose_name='الأيقونة'
    )
    
    # ===================== الربط =====================
    url_name = models.CharField(
        max_length=100,
        help_text='اسم الرابط (مثال: admission:index)',
        verbose_name='اسم الرابط'
    )
    
    # ===================== الحالة =====================
    is_active = models.BooleanField(
        default=True,
        help_text='إذا كان غير مفعل، يظهر "قريباً"',
        verbose_name='مفعّل'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب'
    )
    
    # ===================== تواريخ =====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخر تحديث'
    )
    
    class Meta:
        verbose_name = 'خدمة'
        verbose_name_plural = 'الخدمات'
        ordering = ['order', 'title']
    
    def __str__(self):
        status = '✅' if self.is_active else '⏸️'
        return f'{status} {self.title}'


class QuickLink(models.Model):
    """
    الروابط السريعة (في الصفحة الرئيسية)
    """
    
    title = models.CharField(
        max_length=100,
        verbose_name='العنوان'
    )
    
    url = models.CharField(
        max_length=200,
        blank=True,
        help_text='اتركه فارغاً لاستخدام اسم الرابط',
        verbose_name='الرابط المباشر'
    )
    
    url_name = models.CharField(
        max_length=100,
        blank=True,
        help_text='اسم الرابط في Django (مثال: ranks:index)',
        verbose_name='اسم رابط Django'
    )
    
    icon = models.CharField(
        max_length=50,
        default='fa-link',
        verbose_name='الأيقونة'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب'
    )
    
    class Meta:
        verbose_name = 'رابط سريع'
        verbose_name_plural = 'الروابط السريعة'
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
class Announcement(models.Model):
    """
    إعلان يظهر في البانر المتحرك بالصفحة الرئيسية
    """
    title = models.CharField(
        max_length=200,
        verbose_name='عنوان الإعلان',
    )
    description = models.TextField(
        blank=True,
        verbose_name='الوصف المختصر',
    )
    image = models.ImageField(
        upload_to='announcements/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='صورة الإعلان',
        help_text='المقاس المثالي: 1200×400 بكسل',
    )
    link = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='الرابط',
        help_text='مثال: /ranks/ أو https://example.com',
    )
    button_text = models.CharField(
        max_length=50,
        default='اعرف المزيد',
        blank=True,
        verbose_name='نص الزر',
    )
    bg_color = models.CharField(
        max_length=50,
        default='linear-gradient(135deg, #1e40af, #3b82f6)',
        blank=True,
        verbose_name='لون الخلفية',
        help_text='CSS gradient أو لون عادي',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )
    starts_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='يبدأ من',
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='ينتهي في',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء',
    )

    class Meta:
        verbose_name = 'إعلان'
        verbose_name_plural = 'الإعلانات'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_visible(self):
        """هل الإعلان مرئي الآن؟"""
        from django.utils import timezone
        now = timezone.now()

        if not self.is_active:
            return False
        if self.starts_at and now < self.starts_at:
            return False
        if self.expires_at and now > self.expires_at:
            return False
        return True