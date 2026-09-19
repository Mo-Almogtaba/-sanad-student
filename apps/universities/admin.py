from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import University, Faculty, AdmissionRequirement


# =========================================================
# إدارة الجامعات
# =========================================================
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    
    list_display = [
        'name',
        'city',
        'get_type_badge',
        'get_faculties_count',
        'is_active',
        'order',
    ]
    
    list_filter = [
        'university_type',
        'city',
        'is_active',
    ]
    
    search_fields = [
        'name',
        'name_en',
        'city',
    ]
    
    list_editable = ['is_active', 'order']
    list_display_links = ['name']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'name_en', 'slug', 'university_type')
        }),
        ('الموقع والتواصل', {
            'fields': ('city', 'website')
        }),
        ('التفاصيل', {
            'fields': ('description', 'established_year')
        }),
        ('الصور', {
            'fields': ('logo',)
        }),
        ('الحالة', {
            'fields': ('is_active', 'order')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['activate_universities', 'deactivate_universities']
    
    @admin.display(description='النوع')
    def get_type_badge(self, obj):
        colors = {
            'government': '#007bff',
            'private': '#7c3aed',
            'international': '#28a745',
        }
        color = colors.get(obj.university_type, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.85em;">{}</span>',
            color,
            obj.get_university_type_display()
        )
    
    @admin.display(description='عدد الكليات')
    def get_faculties_count(self, obj):
        count = obj.faculties_count
        return format_html(
            '<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            count
        )
    
    @admin.action(description='✅ تفعيل الجامعات المحددة')
    def activate_universities(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ تم تفعيل {updated} جامعة')
    
    @admin.action(description='❌ تعطيل الجامعات المحددة')
    def deactivate_universities(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'❌ تم تعطيل {updated} جامعة')


# =========================================================
# إدارة الكليات
# =========================================================
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    
    list_display = [
        'name',
        'get_university',
        'get_parent',
        'get_category_badge',
        'duration_years',
        'get_latest_min',
        'is_active',
    ]
    
    list_filter = [
        'university',
        'category',
        'is_active',
        'duration_years',
    ]
    
    search_fields = [
        'name',
        'name_en',
        'university__name',
    ]
    
    list_editable = ['is_active']
    ordering = ['university', 'order', 'name']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('university', 'parent_faculty', 'name', 'name_en', 'slug')
        }),
        ('التصنيف والتفاصيل', {
            'fields': ('category', 'duration_years')
        }),
        ('الحالة والترتيب', {
            'fields': ('is_active', 'order')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['activate_faculties', 'deactivate_faculties']
    
    @admin.display(description='الجامعة')
    def get_university(self, obj):
        return obj.university.name
    
    @admin.display(description='الكلية الأم')
    def get_parent(self, obj):
        if obj.parent_faculty:
            return obj.parent_faculty.name
        return '—'
    
    @admin.display(description='التصنيف')
    def get_category_badge(self, obj):
        colors = {
            'medical': '#dc3545',
            'engineering': '#fd7e14',
            'humanities': '#6f42c1',
            'administrative': '#007bff',
            'science': '#17a2b8',
            'technology': '#6c757d',
            'agriculture': '#28a745',
            'law': '#343a40',
            'education': '#ffc107',
            'art': '#e83e8c',
            'other': '#6c757d',
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-size: 0.85em;">{}</span>',
            color,
            obj.get_category_display()
        )
    
    @admin.display(description='أحدث حد أدنى')
    def get_latest_min(self, obj):
        latest = obj.requirements.order_by('-year').first()
        if latest:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 10px;">{}%</span>',
                latest.min_percentage
            )
        return mark_safe('<span style="color: #999;">—</span>')
    
    @admin.action(description='✅ تفعيل الكليات المحددة')
    def activate_faculties(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ تم تفعيل {updated} كلية')
    
    @admin.action(description='❌ تعطيل الكليات المحددة')
    def deactivate_faculties(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'❌ تم تعطيل {updated} كلية')


# =========================================================
# إدارة متطلبات القبول
# =========================================================
@admin.register(AdmissionRequirement)
class AdmissionRequirementAdmin(admin.ModelAdmin):
    
    list_display = [
        'get_faculty',
        'get_university',
        'year',
        'get_stream_badge',
        'min_percentage',
        'seats_available',
    ]
    
    list_filter = [
        'year',
        'stream',
        'faculty__university',
        'faculty__category',
    ]
    
    search_fields = [
        'faculty__name',
        'faculty__university__name',
    ]
    
    list_editable = ['min_percentage', 'seats_available']
    ordering = ['-year', 'faculty__university', 'faculty__name']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('faculty', 'year', 'stream')
        }),
        ('النسبة والمقاعد', {
            'fields': ('min_percentage', 'seats_available')
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['copy_to_next_year']
    
    @admin.display(description='الكلية')
    def get_faculty(self, obj):
        return obj.faculty.name
    
    @admin.display(description='الجامعة')
    def get_university(self, obj):
        return obj.faculty.university.name
    
    @admin.display(description='المساق')
    def get_stream_badge(self, obj):
        colors = {
            'scientific': '#007bff',
            'literary': '#6f42c1',
            'general': '#6c757d',
        }
        color = colors.get(obj.stream, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 8px; font-size: 0.8em;">{}</span>',
            color,
            obj.get_stream_display()
        )
    
    @admin.action(description='📋 نسخ إلى السنة التالية')
    def copy_to_next_year(self, request, queryset):
        count = 0
        for req in queryset:
            next_year = req.year + 1
            exists = AdmissionRequirement.objects.filter(
                faculty=req.faculty,
                year=next_year,
                stream=req.stream
            ).exists()
            
            if not exists:
                AdmissionRequirement.objects.create(
                    faculty=req.faculty,
                    year=next_year,
                    stream=req.stream,
                    min_percentage=req.min_percentage,
                    seats_available=req.seats_available,
                    notes=f'منسوخ من سنة {req.year}'
                )
                count += 1
        
        self.message_user(request, f'✅ تم نسخ {count} متطلب للسنة التالية')


# =========================================================
# عناوين لوحة الإدارة
# =========================================================
admin.site.site_header = "لوحة إدارة توب سينير"
admin.site.site_title = "توب سينير"
admin.site.index_title = "إدارة النظام"