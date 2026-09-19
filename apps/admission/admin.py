from django.contrib import admin
from django.utils.html import format_html
from .models import UniversityApplication


@admin.register(UniversityApplication)
class UniversityApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'application_code', 'full_name', 'seat_number',
        'phone_number', 'state_display_admin', 'exam_year',
        'stream_display_admin', 'type_badge', 'status_badge', 'submitted_at',
    ]
    list_filter = ['status', 'state', 'exam_year', 'stream', 'application_type', 'submitted_at']
    search_fields = ['application_code', 'full_name', 'seat_number', 'phone_number']
    readonly_fields = ['application_code', 'submitted_at']
    list_per_page = 50
    date_hierarchy = 'submitted_at'

    fieldsets = (
        ('رقم الطلب', {
            'fields': ('application_code', 'submitted_at', 'status')
        }),
        ('بيانات الطالب', {
            'fields': ('full_name', 'seat_number', 'phone_number')
        }),
        ('بيانات الامتحان', {
            'fields': ('state', 'exam_year', 'stream', 'optional_subject')
        }),
        ('نوع التقديم', {
            'fields': ('application_type', 'failed_subjects')
        }),
        ('المرفقات', {
            'fields': ('preferences_file',)
        }),
        ('ملاحظات الإدارة', {
            'fields': ('admin_notes',)
        }),
    )

    actions = ['mark_as_reviewed', 'mark_as_accepted', 'mark_as_rejected']

    @admin.display(description='الولاية')
    def state_display_admin(self, obj):
        return obj.state_display

    @admin.display(description='المساق')
    def stream_display_admin(self, obj):
        return obj.stream_display

    @admin.display(description='النوع')
    def type_badge(self, obj):
        colors = {'bachelor': '#007bff', 'diploma': '#6f42c1'}
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.application_type, '#6c757d'),
            obj.type_display
        )

    @admin.display(description='الحالة')
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'reviewed': '#17a2b8',
            'accepted': '#28a745',
            'rejected': '#dc3545',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )

    @admin.action(description='✅ قيد المراجعة')
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(status='reviewed')
        self.message_user(request, f'✅ تم تحديث {updated} طلب')

    @admin.action(description='✅ قبول')
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'✅ تم قبول {updated} طلب')

    @admin.action(description='❌ رفض')
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'❌ تم رفض {updated} طلب')