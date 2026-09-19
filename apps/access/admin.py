from django.contrib import admin
from django.utils.html import format_html
from .models import AccessCode, GuestUsage


@admin.register(AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    list_display = [
        'request_code', 'full_name', 'phone_number',
        'status_badge', 'code', 'usage_info', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'phone_number', 'code', 'request_code']
    readonly_fields = ['request_code', 'created_at', 'approved_at']
    list_per_page = 50

    fieldsets = (
        ('معلومات الطلب', {
            'fields': ('request_code', 'full_name', 'phone_number', 'created_at')
        }),
        ('الكود والموافقة', {
            'fields': ('code', 'status', 'approved_at')
        }),
        ('الحدود', {
            'fields': ('max_uses', 'current_uses', 'expires_at')
        }),
    )

    actions = ['approve_selected', 'reject_selected']

    @admin.display(description='الحالة')
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'active': '#28a745',
            'expired': '#dc3545',
            'rejected': '#6c757d',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )

    @admin.display(description='الاستخدام')
    def usage_info(self, obj):
        return f"{obj.current_uses}/{obj.max_uses}"

    @admin.action(description='✅ موافقة (إنشاء كود)')
    def approve_selected(self, request, queryset):
        count = 0
        for obj in queryset.filter(status='pending'):
            obj.status = 'active'
            obj.save()
            count += 1
        self.message_user(request, f'✅ تمت الموافقة على {count} طلب')

    @admin.action(description='❌ رفض')
    def reject_selected(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'❌ تم رفض {updated} طلب')


@admin.register(GuestUsage)
class GuestUsageAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'usage_count', 'activated_code', 'first_seen', 'last_seen']
    list_filter = ['last_seen']
    search_fields = ['ip_address', 'activated_code']
    readonly_fields = ['identifier', 'ip_address', 'first_seen', 'last_seen']
    list_per_page = 100