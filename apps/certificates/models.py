from django.db import models


class CertificateRequest(models.Model):
    """
    طلب خدمة شهادات (استخراج / توثيق / ترجمة)
    """
    
    SERVICE_CHOICES = [
        ('high_school', 'استخراج شهادة ثانوية'),
        ('university', 'استخراج شهادة جامعية'),
        ('verify', 'توثيق شهادة'),
        ('translate', 'ترجمة معتمدة'),
        ('replace', 'بدل فاقد'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'جديد'),
        ('processing', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغي'),
    ]
    
    # ===================== رقم الطلب =====================
    request_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الطلب',
    )
    
    # ===================== البيانات الأساسية =====================
    full_name = models.CharField(
        max_length=200,
        verbose_name='الاسم الرباعي',
    )
    
    phone_number = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف (واتساب)',
    )
    
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
        verbose_name='نوع الخدمة',
    )
    
    # ===================== تفاصيل إضافية =====================
    details = models.TextField(
        blank=True,
        verbose_name='تفاصيل إضافية',
        help_text='أي معلومات مهمة عن الطلب'
    )
    
    # ===================== المرفقات =====================
    certificate_file = models.FileField(
        upload_to='certificates/certificate/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='صورة الشهادة',
    )
    
    national_id_file = models.FileField(
        upload_to='certificates/national_id/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='الرقم الوطني',
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
        verbose_name='تاريخ الطلب',
    )
    
    class Meta:
        verbose_name = 'طلب شهادة'
        verbose_name_plural = 'طلبات الشهادات'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.request_code} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        # توليد رقم طلب فريد
        if not self.request_code:
            import random
            while True:
                code = f"CERT-{random.randint(100000, 999999)}"
                if not CertificateRequest.objects.filter(request_code=code).exists():
                    self.request_code = code
                    break
        
        # تنظيف رقم الهاتف
        if self.phone_number:
            self.phone_number = self.phone_number.replace('+', '').replace(' ', '').replace('-', '')
            if not self.phone_number.startswith('249'):
                self.phone_number = '249' + self.phone_number.lstrip('0')
        
        super().save(*args, **kwargs)
    
    @property
    def service_display(self):
        """اسم الخدمة"""
        return dict(self.SERVICE_CHOICES).get(self.service_type, self.service_type)