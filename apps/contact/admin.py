from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'message_code', 'full_name', 'phone_number',
        'service_badge', 'scope_badge', 'status_badge', 'submitted_at',
    ]
    list_filter = ['status', 'service_type', 'scope', 'submitted_at']
    search_fields = ['message_code', 'full_name', 'phone_number', 'message']
    readonly_fields = ['message_code', 'submitted_at']
    list_per_page = 50
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('رقم الرسالة', {
            'fields': ('message_code', 'submitted_at', 'status')
        }),
        ('بيانات المرسل', {
            'fields': ('full_name', 'phone_number')
        }),
        ('تفاصيل الرسالة', {
            'fields': ('service_type', 'scope', 'message')
        }),
        ('ملاحظات الإدارة', {
            'fields': ('admin_notes',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']
    
    @admin.display(description='الخدمة')
    def service_badge(self, obj):
        colors = {
            'ranks': '#28a745',
            'admission': '#007bff',
            'certificates': '#17a2b8',
            'scholarships': '#ffc107',
            'general': '#6c757d',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.service_type, '#6c757d'),
            obj.service_display
        )
    
    @admin.display(description='النطاق')
    def scope_badge(self, obj):
        colors = {
            'inquiry': '#17a2b8',
            'complaint': '#dc3545',
            'suggestion': '#28a745',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.scope, '#6c757d'),
            obj.scope_display
        )
    
    @admin.display(description='الحالة')
    def status_badge(self, obj):
        colors = {
            'new': '#ffc107',
            'read': '#17a2b8',
            'replied': '#28a745',
            'archived': '#6c757d',
        }
        return format_html(
            '<span style="background:{}; color:white; padding:3px 10px; border-radius:10px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    
    @admin.action(description='📖 تم القراءة')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'✅ تم تحديث {updated} رسالة')
    
    @admin.action(description='✅ تم الرد')
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'✅ تم تحديث {updated} رسالة')
    
    @admin.action(description='📦 أرشفة')
    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'📦 تم أرشفة {updated} رسالة')