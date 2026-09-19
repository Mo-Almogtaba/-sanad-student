from django.contrib import admin
from django.utils.html import format_html
from .models import CertificateRequest


@admin.register(CertificateRequest)
class CertificateRequestAdmin(admin.ModelAdmin):
    list_display = [
        'request_code', 'full_name', 'phone_number',
        'service_badge', 'status_badge', 'submitted_at',
    ]
    list_filter = ['status', 'service_type', 'submitted_at']
    search_fields = ['request_code', 'full_name', 'phone_number']
    readonly_fields = ['request_code', 'submitted_at']
    list_per_page = 50
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('رقم الطلب', {
            'fields': ('request_code', 'submitted_at', 'status')
        }),
        ('بيانات العميل', {
            'fields': ('full_name', 'phone_number')
        }),
        ('تفاصيل الخدمة', {
            'fields': ('service_type', 'details')
        }),
        ('المرفقات', {
            'fields': ('certificate_file', 'national_id_file')
        }),
        ('ملاحظات الإدارة', {
            'fields': ('admin_notes',)
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_completed', 'mark_as_cancelled']
    
    @admin.display(description='الخدمة')
    def service_badge(self, obj):
        colors = {
            'high_school': '#007bff',
            'university': '#28a745',
            'verify': '#17a2b8',
            'translate': '#6f42c1',
            'replace': '#ffc107',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.service_type, '#6c757d'),
            obj.service_display
        )
    
    @admin.display(description='الحالة')
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'processing': '#17a2b8',
            'completed': '#28a745',
            'cancelled': '#dc3545',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    
    @admin.action(description='🔄 قيد التنفيذ')
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'✅ تم تحديث {updated} طلب')
    
    @admin.action(description='✅ مكتمل')
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'✅ تم إكمال {updated} طلب')
    
    @admin.action(description='❌ ملغي')
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'❌ تم إلغاء {updated} طلب')