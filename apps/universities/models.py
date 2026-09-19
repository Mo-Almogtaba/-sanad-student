from django.db import models
from django.utils.text import slugify


class University(models.Model):
    """
    نموذج الجامعة
    """
    
    UNIVERSITY_TYPE_CHOICES = [
        ('government', 'حكومية'),
        ('private', 'خاصة'),
        ('international', 'دولية'),
    ]
    
    # ✅ المعلومات الأساسية
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='اسم الجامعة'
    )
    
    name_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='الاسم بالإنجليزية'
    )
    
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        verbose_name='الرابط المختصر'
    )
    
    # ✅ الموقع
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='المدينة'
    )
    
    # ✅ التواصل
    website = models.URLField(
        blank=True,
        verbose_name='الموقع الإلكتروني'
    )
    
    # ✅ التفاصيل
    description = models.TextField(
        blank=True,
        verbose_name='نبذة عن الجامعة'
    )
    
    established_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='سنة التأسيس'
    )
    
    university_type = models.CharField(
        max_length=20,
        choices=UNIVERSITY_TYPE_CHOICES,
        default='government',
        verbose_name='نوع الجامعة'
    )
    
    # ✅ الصور
    logo = models.ImageField(
        upload_to='universities/logos/',
        blank=True,
        null=True,
        verbose_name='شعار الجامعة'
    )
    
    # ✅ الحالة والترتيب
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشطة'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب'
    )
    
    # ✅ تواريخ
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        verbose_name = 'جامعة'
        verbose_name_plural = 'الجامعات'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """إنشاء slug تلقائياً عند الحفظ"""
        if not self.slug:
            base_slug = slugify(self.name_en or self.name)
            slug = base_slug
            counter = 1
            while University.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    @property
    def faculties_count(self):
        """عدد الكليات"""
        return self.faculties.filter(is_active=True).count()


class Faculty(models.Model):
    """
    نموذج الكلية/التخصص
    """
    
    CATEGORY_CHOICES = [
        ('medical', 'طبي'),
        ('engineering', 'هندسي'),
        ('humanities', 'أدبي'),
        ('administrative', 'إداري'),
        ('science', 'علوم'),
        ('technology', 'تقنية'),
        ('agriculture', 'زراعي'),
        ('law', 'قانون'),
        ('education', 'تربية'),
        ('art', 'فنون'),
        ('other', 'أخرى'),
    ]
    
    # ✅ العلاقة بالجامعة
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='faculties',
        verbose_name='الجامعة'
    )
    
    # ✅ العلاقة بالكلية الأم (للتخصصات الفرعية)
    parent_faculty = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_faculties',
        verbose_name='الكلية الأم'
    )
    
    # ✅ المعلومات الأساسية
    name = models.CharField(
        max_length=300,
        verbose_name='اسم الكلية/التخصص'
    )
    
    name_en = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='الاسم بالإنجليزية'
    )
    
    slug = models.SlugField(
        max_length=350,
        blank=True,
        verbose_name='الرابط المختصر'
    )
    
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='التصنيف'
    )
    
    duration_years = models.IntegerField(
        default=4,
        verbose_name='مدة الدراسة (سنوات)'
    )
    
    # ✅ الحالة والترتيب
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشطة'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='الترتيب'
    )
    
    # ✅ تواريخ
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        verbose_name = 'كلية'
        verbose_name_plural = 'الكليات'
        ordering = ['university', 'order', 'id']
        unique_together = ['name', 'university', 'parent_faculty']
    
    def __str__(self):
        if self.parent_faculty:
            return f"{self.parent_faculty.name} - {self.name}"
        return f"{self.name} - {self.university.name}"
    
    def save(self, *args, **kwargs):
        """إنشاء slug تلقائياً"""
        if not self.slug:
            base_slug = slugify(self.name_en or self.name)
            slug = f"{base_slug}-{self.university.id}"
            
            if self.parent_faculty:
                slug = f"{slug}-{self.parent_faculty.id}"
            
            original_slug = slug
            counter = 1
            while Faculty.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)


class AdmissionRequirement(models.Model):
    """
    نموذج الحد الأدنى للقبول
    """
    
    STREAM_CHOICES = [
        ('scientific', 'علمي'),
        ('literary', 'أدبي'),
        ('general', 'عام'),
    ]
    
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='requirements',
        verbose_name='الكلية/التخصص'
    )
    
    year = models.IntegerField(
        verbose_name='سنة القبول',
        help_text='مثال: 2024'
    )
    
    stream = models.CharField(
        max_length=20,
        choices=STREAM_CHOICES,
        default='general',
        verbose_name='المساق',
        help_text='اتركه "عام" إذا كانت النسبة واحدة لجميع المساقات'
    )
    
    min_percentage = models.FloatField(
        verbose_name='الحد الأدنى للنسبة (%)',
        help_text='النسبة المئوية المطلوبة للقبول'
    )
    
    seats_available = models.IntegerField(
        default=0,
        verbose_name='عدد المقاعد',
        help_text='0 = غير معروف'
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name='ملاحظات'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    class Meta:
        verbose_name = 'متطلب قبول'
        verbose_name_plural = 'متطلبات القبول'
        ordering = ['-year', 'faculty']
        unique_together = ['faculty', 'year', 'stream']
    
    def __str__(self):
        return f"{self.faculty.name} - {self.year} - {self.min_percentage}%"