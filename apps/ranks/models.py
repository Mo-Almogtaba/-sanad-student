from django.db import models
from django.utils.text import slugify


class ProbabilityLevel(models.Model):
    """
    مستويات الاحتمالية القابلة للتعديل
    مثال: "عالية جداً" من +10% فما فوق
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='اسم المستوى',
        help_text='مثال: عالية جداً'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='الرمز'
    )
    
    min_difference = models.FloatField(
        verbose_name='الحد الأدنى للفرق (%)',
        help_text='الفرق بين نسبة الطالب والحد الأدنى (يُحسب كـ: نسبة الطالب - الحد الأدنى)',
    )
    
    max_difference = models.FloatField(
        null=True,
        blank=True,
        verbose_name='الحد الأعلى للفرق (%)',
        help_text='اتركه فارغاً إذا كان مستوى مفتوحاً (بدون حد أعلى)'
    )
    
    color = models.CharField(
        max_length=20,
        default='#6c757d',
        verbose_name='اللون',
        help_text='مثال: #28a745'
    )
    
    icon = models.CharField(
        max_length=50,
        default='bi-circle',
        blank=True,
        verbose_name='الأيقونة',
        help_text='مثال: bi-check-circle'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب',
        help_text='الأقل = الأعلى في العرض'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='مفعّل'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    class Meta:
        verbose_name = 'مستوى احتمالية'
        verbose_name_plural = 'مستويات الاحتمالية'
        ordering = ['order']
    
    def __str__(self):
        if self.max_difference is not None:
            return f"{self.name} ({self.min_difference}% إلى {self.max_difference}%)"
        return f"{self.name} ({self.min_difference}% فأكثر)"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ProbabilityLevel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def matches_difference(self, difference):
        """
        هل الفرق ينتمي لهذا المستوى؟
        """
        if difference < self.min_difference:
            return False
        if self.max_difference is not None and difference >= self.max_difference:
            return False
        return True


class Preference(models.Model):
    """
    رغبة الطالب
    """
    
    # ✅ معلومات الطالب
    student_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='اسم الطالب (اختياري)'
    )
    
    student_percentage = models.FloatField(
        verbose_name='نسبة الطالب (%)'
    )
    
    student_stream = models.CharField(
        max_length=20,
        choices=[
            ('scientific', 'علمي'),
            ('literary', 'أدبي'),
        ],
        default='scientific',
        verbose_name='المساق'
    )
    
    # ✅ العلاقة بالكلية
    faculty = models.ForeignKey(
        'universities.Faculty',
        on_delete=models.CASCADE,
        related_name='preferences',
        verbose_name='الكلية/التخصص'
    )
    
    priority = models.IntegerField(
        verbose_name='الأولوية',
        help_text='رقم الرغبة (1، 2، 3...)'
    )
    
    # ✅ الحالة
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )
    
    class Meta:
        verbose_name = 'رغبة'
        verbose_name_plural = 'الرغبات'
        ordering = ['priority']
    
    def __str__(self):
        return f"{self.student_name or 'طالب'} - رغبة #{self.priority} - {self.faculty.name}"


class PredictionSession(models.Model):
    """
    جلسة توقع (تُخزّن نتيجة توقع واحدة)
    """
    
    student_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='اسم الطالب'
    )
    
    student_percentage = models.FloatField(
        verbose_name='نسبة الطالب (%)'
    )
    
    student_stream = models.CharField(
        max_length=20,
        choices=[
            ('scientific', 'علمي'),
            ('literary', 'أدبي'),
        ],
        default='scientific',
        verbose_name='المساق'
    )
    
    session_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='كود الجلسة',
        help_text='كود فريد لمشاركة النتائج'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ التوقع'
    )
    
    class Meta:
        verbose_name = 'جلسة توقع'
        verbose_name_plural = 'جلسات التوقع'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student_name or 'طالب'} - {self.student_percentage}% - {self.created_at.strftime('%Y-%m-%d')}"


class PredictionResult(models.Model):
    """
    نتيجة توقع لكل رغبة
    """
    
    session = models.ForeignKey(
        PredictionSession,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='الجلسة'
    )
    
    faculty = models.ForeignKey(
        'universities.Faculty',
        on_delete=models.CASCADE,
        verbose_name='الكلية'
    )
    
    priority = models.IntegerField(
        verbose_name='الأولوية'
    )
    
    student_percentage = models.FloatField(
        verbose_name='نسبة الطالب'
    )
    
    min_percentage = models.FloatField(
        verbose_name='الحد الأدنى'
    )
    
    difference = models.FloatField(
        verbose_name='الفرق',
        help_text='نسبة الطالب - الحد الأدنى'
    )
    
    probability_level = models.ForeignKey(
        ProbabilityLevel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='مستوى الاحتمالية'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    class Meta:
        verbose_name = 'نتيجة توقع'
        verbose_name_plural = 'نتائج التوقع'
        ordering = ['priority']
    
    def __str__(self):
        return f"{self.faculty.name} - {self.difference:+.1f}%"