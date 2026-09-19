from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Section, UserProfile


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['icon_preview', 'name', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['name']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} if False else {}

    @admin.display(description='الأيقونة')
    def icon_preview(self, obj):
        return format_html('<i class="fa {}"></i>', obj.icon)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'الصلاحيات'
    verbose_name_plural = 'الصلاحيات'
    filter_horizontal = ('sections',)
    fieldsets = (
        ('الدور', {
            'fields': ('role', 'is_active')
        }),
        ('الأقسام المصرح بها', {
            'fields': ('sections',),
            'description': 'حدد الأقسام التي يمكن للمستخدم الوصول إليها'
        }),
        ('معلومات إضافية', {
            'fields': ('phone', 'job_title')
        }),
    )


# ✅ إعادة تسجيل UserAdmin مع UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'get_full_name', 'get_role', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'profile__role']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    @admin.display(description='الدور')
    def get_role(self, obj):
        try:
            role = obj.profile.get_role_display()
            colors = {
                'مدير عام': '#dc3545',
                'قائد فريق': '#007bff',
                'موظف': '#28a745',
            }
            return format_html(
                '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
                colors.get(role, '#6c757d'),
                role
            )
        except Exception:
            return '—'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ✅ تحديث عناوين لوحة الإدارة
admin.site.site_header = "سند الطالب - لوحة الإدارة"
admin.site.site_title = "سند الطالب"
admin.site.index_title = "إدارة النظام"