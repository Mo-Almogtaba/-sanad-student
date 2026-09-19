from django.db import models
from django.contrib.auth.models import User


class ActivityLog(models.Model):
    """
    سجل نشاط المشرفين
    """
    ACTION_CHOICES = [
        ('view', 'عرض'),
        ('create', 'إنشاء'),
        ('update', 'تعديل'),
        ('delete', 'حذف'),
        ('status_change', 'تغيير الحالة'),
        ('export', 'تصدير'),
    ]

    TARGET_CHOICES = [
        ('application', 'طلب تقديم'),
        ('certificate', 'طلب شهادة'),
        ('contact', 'رسالة تواصل'),
        ('access_code', 'كود وصول'),
        ('user', 'مستخدم'),
        ('announcement', 'إعلان'), 
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='activities',
        verbose_name='المستخدم',
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name='الإجراء',
    )
    target_type = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        verbose_name='نوع الهدف',
    )
    target_id = models.IntegerField(
        verbose_name='رقم الهدف',
    )
    details = models.TextField(
        blank=True,
        verbose_name='التفاصيل',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='التاريخ',
    )

    class Meta:
        verbose_name = 'سجل نشاط'
        verbose_name_plural = 'سجل الأنشطة'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username if self.user else 'مجهول'} - {self.get_action_display()} - {self.created_at}"