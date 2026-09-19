import hashlib
import random
import string
from datetime import timedelta

from django.db import models
from django.utils import timezone


class AccessCode(models.Model):
    """
    كود وصول - يشمل الطلب والتفعيل في نموذج واحد
    """
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('active', 'مفعّل'),
        ('expired', 'منتهي'),
        ('rejected', 'مرفوض'),
    ]

    # ===================== بيانات الطلب =====================
    request_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='كود الطلب',
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='الاسم الكامل',
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الهاتف',
    )

    # ===================== الكود (يُملأ عند الموافقة) =====================
    code = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        verbose_name='كود الوصول',
    )

    # ===================== الحالة =====================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة',
    )

    # ===================== الحدود =====================
    max_uses = models.IntegerField(
        default=20,
        verbose_name='عدد المحاولات',
    )
    current_uses = models.IntegerField(
        default=0,
        verbose_name='المستخدم',
    )

    # ===================== المدة =====================
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاريخ الانتهاء',
    )

    # ===================== التواريخ =====================
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الطلب',
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاريخ الموافقة',
    )

    class Meta:
        verbose_name = 'كود وصول'
        verbose_name_plural = 'أكواد الوصول'
        ordering = ['-created_at']

    def __str__(self):
        if self.code:
            return f"{self.code} - {self.full_name}"
        return f"{self.request_code} - {self.full_name}"

    def save(self, *args, **kwargs):
        # توليد كود الطلب
        if not self.request_code:
            self.request_code = self._generate_request_code()

        # توليد كود الوصول عند الموافقة
        if self.status == 'active' and not self.code:
            self.code = self._generate_code()
            self.approved_at = timezone.now()
            if not self.expires_at:
                self.expires_at = timezone.now() + timedelta(days=30)

        super().save(*args, **kwargs)

    def _generate_request_code(self):
        """توليد كود طلب فريد: REQ-XXXX"""
        while True:
            code = f"REQ-{random.randint(1000, 9999)}"
            if not AccessCode.objects.filter(request_code=code).exists():
                return code

    def _generate_code(self):
        """توليد كود وصول: SANAD-XXXX-XXXX-XXXX"""
        while True:
            parts = [
                ''.join(random.choices(string.ascii_uppercase, k=4)),
                ''.join(random.choices(string.digits, k=4)),
                ''.join(random.choices(string.ascii_uppercase, k=4)),
            ]
            code = f"SANAD-{parts[0]}-{parts[1]}-{parts[2]}"
            if not AccessCode.objects.filter(code=code).exists():
                return code

    @property
    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False

    @property
    def can_use(self):
        if self.status != 'active':
            return False
        if self.is_expired:
            return False
        if self.current_uses >= self.max_uses:
            return False
        return True

    @property
    def remaining_uses(self):
        return max(0, self.max_uses - self.current_uses)

    def use(self):
        """تسجيل استخدام"""
        self.current_uses += 1
        self.save(update_fields=['current_uses'])


class GuestUsage(models.Model):
    """
    تتبع استخدام الزوار (المحاولة المجانية)
    """
    FREE_LIMIT = 1

    identifier = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='المعرف',
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='IP',
    )
    usage_count = models.IntegerField(
        default=0,
        verbose_name='عدد المحاولات',
    )
    activated_code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='الكود المُفعّل',
    )
    first_seen = models.DateTimeField(
        auto_now_add=True,
        verbose_name='أول ظهور',
    )
    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name='آخر ظهور',
    )

    class Meta:
        verbose_name = 'استخدام زائر'
        verbose_name_plural = 'استخدامات الزوار'
        ordering = ['-last_seen']

    def __str__(self):
        return f"{self.ip_address} ({self.usage_count})"

    @property
    def can_use_free(self):
        return self.usage_count < self.FREE_LIMIT and not self.activated_code

    @property
    def can_use_paid(self):
        if not self.activated_code:
            return False
        code = self.get_code()
        return code.can_use if code else False

    @property
    def can_use_any(self):
        if self.activated_code:
            return self.can_use_paid
        return self.can_use_free

    def get_code(self):
        if not self.activated_code:
            return None
        try:
            return AccessCode.objects.get(code=self.activated_code)
        except AccessCode.DoesNotExist:
            return None

    def use(self):
        """تسجيل استخدام"""
        if self.activated_code:
            code = self.get_code()
            if code:
                code.use()
        else:
            self.usage_count += 1
            self.save(update_fields=['usage_count'])

    @staticmethod
    def get_for_request(request):
        """الحصول على GuestUsage للطلب الحالي"""
        ip = GuestUsage._get_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')[:200]
        identifier = hashlib.sha256(f"{ip}:{ua}".encode()).hexdigest()

        obj, _ = GuestUsage.objects.get_or_create(
            identifier=identifier,
            defaults={'ip_address': ip}
        )
        return obj

    @staticmethod
    def _get_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')