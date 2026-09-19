from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Section(models.Model):
    """
    أقسام الموقع القابلة للتفويض
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='اسم القسم',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='الرمز',
    )
    icon = models.CharField(
        max_length=50,
        default='fa-circle',
        verbose_name='الأيقونة',
        help_text='مثال: fa-file-alt',
    )
    description = models.TextField(
        blank=True,
        verbose_name='الوصف',
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
        verbose_name = 'قسم'
        verbose_name_plural = 'الأقسام'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Section.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """
    بيانات إضافية لكل مستخدم
    """
    ROLE_CHOICES = [
        ('super_admin', 'مدير عام'),
        ('team_lead', 'قائد فريق'),
        ('staff', 'موظف'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='المستخدم',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff',
        verbose_name='الدور',
    )
    sections = models.ManyToManyField(
        Section,
        blank=True,
        related_name='users',
        verbose_name='الأقسام المصرح بها',
        help_text='الأقسام التي يمكن لهذا المستخدم الوصول إليها',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='رقم الهاتف',
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='المسمى الوظيفي',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='نشط',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء',
    )

    class Meta:
        verbose_name = 'ملف مستخدم'
        verbose_name_plural = 'ملفات المستخدمين'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        """هل مدير عام؟"""
        return self.role == 'super_admin' or self.user.is_superuser

    @property
    def is_team_lead(self):
        return self.role == 'team_lead'

    @property
    def is_staff_member(self):
        return self.role == 'staff'

    def has_section_access(self, section_slug):
        """
        هل لديه صلاحية الوصول لقسم معين؟
        """
        # Super admin → كل الأقسام
        if self.is_super_admin:
            return True

        # staff / team_lead → الأقسام المصرح بها
        return self.sections.filter(slug=section_slug, is_active=True).exists()

    def get_accessible_sections(self):
        """الأقسام التي يستطيع الوصول إليها"""
        if self.is_super_admin:
            return Section.objects.filter(is_active=True)
        return self.sections.filter(is_active=True)


# ✅ Signal: إنشاء UserProfile تلقائياً
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """إنشاء UserProfile عند إنشاء مستخدم جديد"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """حفظ UserProfile عند حفظ المستخدم"""
    if hasattr(instance, 'profile'):
        instance.profile.save()