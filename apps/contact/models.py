from django.db import models


class ContactMessage(models.Model):
    """
    رسالة تواصل من زائر
    """
    
    SERVICE_CHOICES = [
        ('ranks', 'ترتيب الرغبات'),
        ('admission', 'التقديم الإلكتروني'),
        ('certificates', 'الشهادات والتوثيق'),
        ('scholarships', 'المنح الدراسية'),
        ('general', 'استفسار عام'),
    ]
    
    SCOPE_CHOICES = [
        ('inquiry', 'استفسار عن خدمة'),
        ('complaint', 'شكوى'),
        ('suggestion', 'اقتراح'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'جديد'),
        ('read', 'تم القراءة'),
        ('replied', 'تم الرد'),
        ('archived', 'مؤرشف'),
    ]
    
    # ===================== رقم الرسالة =====================
    message_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الرسالة',
    )
    
    # ===================== بيانات المرسل =====================
    full_name = models.CharField(
        max_length=200,
        verbose_name='الاسم الكامل',
    )
    
    phone_number = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف (واتساب)',
    )
    
    # ===================== تفاصيل الرسالة =====================
    service_type = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
        verbose_name='نوع الخدمة',
    )
    
    scope = models.CharField(
        max_length=20,
        choices=SCOPE_CHOICES,
        default='inquiry',
        verbose_name='نطاق الاستفسار',
    )
    
    message = models.TextField(
        verbose_name='الرسالة',
    )
    
    # ===================== الحالة =====================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='الحالة',
    )
    
    admin_notes = models.TextField(
        blank=True,
        verbose_name='ملاحظات الإدارة',
    )
    
    # ===================== التواريخ =====================
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإرسال',
    )
    
    class Meta:
        verbose_name = 'رسالة تواصل'
        verbose_name_plural = 'رسائل التواصل'
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.message_code} - {self.full_name}"
    
    def save(self, *args, **kwargs):
        # توليد رقم رسالة فريد
        if not self.message_code:
            import random
            while True:
                code = f"MSG-{random.randint(100000, 999999)}"
                if not ContactMessage.objects.filter(message_code=code).exists():
                    self.message_code = code
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
    
    @property
    def scope_display(self):
        """اسم نطاق الاستفسار"""
        return dict(self.SCOPE_CHOICES).get(self.scope, self.scope)