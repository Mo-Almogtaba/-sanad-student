from django.db import models


class UniversityApplication(models.Model):
    """
    طلب تقديم إلكتروني للجامعات السودانية
    """

    APPLICATION_TYPE_CHOICES = [
        ('bachelor', 'بكالوريوس'),
        ('diploma', 'دبلوم'),
    ]

    STREAM_CHOICES = [
        ('scientific', 'علمي'),
        ('literary', 'أدبي'),
    ]

    STATUS_CHOICES = [
        ('pending', 'جديد'),
        ('reviewed', 'قيد المراجعة'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]

    STATES = [
        ('khartoum', 'الخرطوم'),
        ('jazeera', 'الجزيرة'),
        ('kassala', 'كسلا'),
        ('qadarif', 'القضارف'),
        ('red_sea', 'البحر الأحمر'),
        ('nile_river', 'نهر النيل'),
        ('north_kordofan', 'شمال كردفان'),
        ('south_kordofan', 'جنوب كردفان'),
        ('west_kordofan', 'غرب كردفان'),
        ('north_darfur', 'شمال دارفور'),
        ('south_darfur', 'جنوب دارفور'),
        ('west_darfur', 'غرب دارفور'),
        ('east_darfur', 'شرق دارفور'),
        ('central_darfur', 'وسط دارفور'),
        ('white_nile', 'النيل الأبيض'),
        ('blue_nile', 'النيل الأزرق'),
        ('sennar', 'سنار'),
        ('northern', 'الشمالية'),
    ]

    # ===================== رقم الطلب =====================
    application_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الطلب',
    )

    # ===================== بيانات الطالب =====================
    full_name = models.CharField(
        max_length=200,
        verbose_name='الاسم الرباعي',
    )

    seat_number = models.CharField(
        max_length=30,
        verbose_name='رقم الجلوس',
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف (واتساب)',
    )

    # ===================== بيانات الامتحان =====================
    state = models.CharField(
        max_length=50,
        choices=STATES,
        verbose_name='الولاية',
    )

    exam_year = models.IntegerField(
        verbose_name='سنة الامتحان',
    )

    stream = models.CharField(
        max_length=20,
        choices=STREAM_CHOICES,
        verbose_name='المساق',
    )

    optional_subject = models.CharField(
        max_length=100,
        verbose_name='المادة الاختيارية',
    )

    # ===================== نوع التقديم =====================
    application_type = models.CharField(
        max_length=20,
        choices=APPLICATION_TYPE_CHOICES,
        default='bachelor',
        verbose_name='نوع التقديم',
    )

    failed_subjects = models.TextField(
        blank=True,
        verbose_name='المواد الراسب بها',
        help_text='مطلوب فقط في حالة التقديم للدبلوم',
    )

    # ===================== ترتيب الرغبات =====================
    preferences_file = models.FileField(
        upload_to='admission/preferences/%Y/%m/',
        verbose_name='ملف ترتيب الرغبات',
    )

    # ✅ رابط نتيجة التوقع (اختياري)
    ranks_session_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='كود جلسة التوقع',
        help_text='إذا ربط الطالب نتيجة توقعه'
    )

    # ===================== الحالة =====================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة',
    )

    admin_notes = models.TextField(
        blank=True,
        verbose_name='ملاحظات الإدارة',
    )

    # ===================== التواريخ =====================
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ التقديم',
    )

    class Meta:
        verbose_name = 'طلب تقديم'
        verbose_name_plural = 'طلبات التقديم'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.application_code} - {self.full_name}"

    def save(self, *args, **kwargs):
        # توليد رقم طلب فريد
        if not self.application_code:
            import random
            while True:
                code = f"APP-{random.randint(100000, 999999)}"
                if not UniversityApplication.objects.filter(application_code=code).exists():
                    self.application_code = code
                    break

        # تنظيف رقم الهاتف
        if self.phone_number:
            self.phone_number = self.phone_number.replace('+', '').replace(' ', '').replace('-', '')
            if not self.phone_number.startswith('249'):
                self.phone_number = '249' + self.phone_number.lstrip('0')

        super().save(*args, **kwargs)

    @property
    def state_display(self):
        """عرض اسم الولاية"""
        return dict(self.STATES).get(self.state, self.state)

    @property
    def stream_display(self):
        """عرض المساق"""
        return dict(self.STREAM_CHOICES).get(self.stream, self.stream)

    @property
    def type_display(self):
        """عرض نوع التقديم"""
        return dict(self.APPLICATION_TYPE_CHOICES).get(self.application_type, self.application_type)