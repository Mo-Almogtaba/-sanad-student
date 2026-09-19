from django.db import models
from django.utils import timezone


class GuideSection(models.Model):
    """
    قسم في دليل التقديم (المتطلبات، الشروط، الخطوات، ...)
    """
    title = models.CharField(
        max_length=200,
        verbose_name='عنوان القسم',
    )
    description = models.TextField(
        blank=True,
        verbose_name='وصف مختصر',
        help_text='يظهر تحت العنوان'
    )
    icon = models.CharField(
        max_length=50,
        default='fa-info-circle',
        verbose_name='الأيقونة',
        help_text='مثال: fa-list-check',
    )
    color = models.CharField(
        max_length=20,
        default='#1e40af',
        verbose_name='اللون',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء',
    )

    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'أقسام الدليل'
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title


class GuideCard(models.Model):
    """
    كرت داخل القسم
    """
    CARD_TYPES = [
        ('accordion', 'Accordion (فتح/إغلاق)'),
        ('list', 'قائمة'),
        ('text', 'نص حر'),
        ('links', 'روابط'),
    ]

    section = models.ForeignKey(
        GuideSection,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='القسم',
    )
    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPES,
        default='accordion',
        verbose_name='نوع الكرت',
    )
    title = models.CharField(
        max_length=300,
        verbose_name='العنوان',
    )
    subtitle = models.CharField(
        max_length=400,
        blank=True,
        verbose_name='وصف مختصر',
    )
    content = models.TextField(
        blank=True,
        verbose_name='المحتوى',
        help_text='يدعم HTML بسيط'
    )
    icon = models.CharField(
        max_length=50,
        default='fa-circle',
        blank=True,
        verbose_name='الأيقونة',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )
    is_open_default = models.BooleanField(
        default=False,
        verbose_name='مفتوح افتراضياً',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء',
    )

    class Meta:
        verbose_name = 'كرت'
        verbose_name_plural = 'الكروت'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.section.title} → {self.title}"


class GuideListItem(models.Model):
    """
    عنصر داخل كرت قائمة
    """
    card = models.ForeignKey(
        GuideCard,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='الكرت',
    )
    text = models.CharField(
        max_length=500,
        verbose_name='النص',
    )
    icon = models.CharField(
        max_length=50,
        default='fa-check-circle',
        blank=True,
        verbose_name='الأيقونة',
    )
    icon_color = models.CharField(
        max_length=20,
        default='#10b981',
        blank=True,
        verbose_name='لون الأيقونة',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )

    class Meta:
        verbose_name = 'عنصر قائمة'
        verbose_name_plural = 'عناصر القوائم'
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class GuideLink(models.Model):
    """
    رابط داخل كرت روابط
    """
    card = models.ForeignKey(
        GuideCard,
        on_delete=models.CASCADE,
        related_name='links',
        verbose_name='الكرت',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='عنوان الرابط',
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='وصف الرابط',
    )
    url = models.URLField(
        verbose_name='الرابط',
    )
    icon = models.CharField(
        max_length=50,
        default='fa-link',
        blank=True,
        verbose_name='الأيقونة',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )

    class Meta:
        verbose_name = 'رابط'
        verbose_name_plural = 'الروابط'
        ordering = ['order']

    def __str__(self):
        return self.title


class GuideImage(models.Model):
    """
    صورة مرفقة لكرت
    """
    card = models.ForeignKey(
        GuideCard,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='الكرت',
    )
    image = models.ImageField(
        upload_to='guide/images/%Y/%m/',
        verbose_name='الصورة',
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='وصف الصورة',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )

    class Meta:
        verbose_name = 'صورة'
        verbose_name_plural = 'الصور'
        ordering = ['order']

    def __str__(self):
        return self.caption or f'صورة {self.pk}'


class GuideVideo(models.Model):
    """
    فيديو يوتيوب مدمج
    """
    card = models.ForeignKey(
        GuideCard,
        on_delete=models.CASCADE,
        related_name='videos',
        blank=True,
        null=True,
        verbose_name='الكرت (اختياري)',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='عنوان الفيديو',
    )
    youtube_url = models.URLField(
        verbose_name='رابط يوتيوب',
        help_text='مثال: https://www.youtube.com/watch?v=XXXXX',
    )
    youtube_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='معرف الفيديو',
        help_text='يُستخرج تلقائياً من الرابط',
    )
    description = models.TextField(
        blank=True,
        verbose_name='وصف',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل',
    )

    class Meta:
        verbose_name = 'فيديو'
        verbose_name_plural = 'الفيديوهات'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # استخراج youtube_id تلقائياً
        if self.youtube_url and not self.youtube_id:
            import re
            patterns = [
                r'(?:youtube\.com\/watch\?v=)([\w-]+)',
                r'(?:youtu\.be\/)([\w-]+)',
                r'(?:youtube\.com\/embed\/)([\w-]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.youtube_url)
                if match:
                    self.youtube_id = match.group(1)
                    break
        super().save(*args, **kwargs)

    @property
    def embed_url(self):
        """رابط التضمين"""
        if self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}"
        return ''


class ImportantDate(models.Model):
    """
    موعد زمني مهم (يظهر مع عداد تنازلي)
    """
    title = models.CharField(
        max_length=200,
        verbose_name='العنوان',
        help_text='مثال: بدء التقديم الإلكتروني'
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='وصف مختصر',
    )
    date = models.DateTimeField(
        verbose_name='التاريخ والوقت',
    )
    icon = models.CharField(
        max_length=50,
        default='fa-calendar-alt',
        blank=True,
        verbose_name='الأيقونة',
    )
    color = models.CharField(
        max_length=20,
        default='#dc2626',
        verbose_name='اللون',
    )
    show_countdown = models.BooleanField(
        default=True,
        verbose_name='إظهار عداد تنازلي',
    )
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل',
    )

    class Meta:
        verbose_name = 'موعد مهم'
        verbose_name_plural = 'المواعيد المهمة'
        ordering = ['date', 'order']

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

    @property
    def is_past(self):
        """هل انتهى الموعد؟"""
        return timezone.now() > self.date

    @property
    def is_today(self):
        """هل هو اليوم؟"""
        return timezone.now().date() == self.date.date()

    @property
    def days_remaining(self):
        """الأيام المتبقية"""
        if self.is_past:
            return 0
        delta = self.date - timezone.now()
        return delta.days