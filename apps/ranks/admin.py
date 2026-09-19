from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import ProbabilityLevel, Preference, PredictionSession, PredictionResult


# =========================================================
# إدارة مستويات الاحتمالية
# =========================================================
@admin.register(ProbabilityLevel)
class ProbabilityLevelAdmin(admin.ModelAdmin):
    """
    إدارة مستويات الاحتمالية القابلة للتعديل
    """
    
    list_display = [
        'get_color_preview',
        'name',
        'get_range',
        'order',
        'is_active',
    ]
    
    list_editable = ['order', 'is_active']
    list_display_links = ['name']
    ordering = ['order']
    
    search_fields = ['name']
    list_filter = ['is_active']
    
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'slug')
        }),
        ('نطاق الفرق', {
            'fields': ('min_difference', 'max_difference'),
            'description': 'الفرق = نسبة الطالب - الحد الأدنى للقبول'
        }),
        ('العرض البصري', {
            'fields': ('color', 'icon', 'order')
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
        ('التواريخ', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
    
    actions = ['activate_levels', 'deactivate_levels']
    
    @admin.display(description='🎨')
    def get_color_preview(self, obj):
        return format_html(
            '<span style="display: inline-block; width: 30px; height: 30px; background: {}; border-radius: 50%; border: 2px solid #ddd;"></span>',
            obj.color
        )
    
    @admin.display(description='النطاق')
    def get_range(self, obj):
        if obj.max_difference is not None:
            return f"من {obj.min_difference}% إلى {obj.max_difference}%"
        return f"من {obj.min_difference}% فأكثر"
    
    @admin.action(description='✅ تفعيل المستويات المحددة')
    def activate_levels(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ تم تفعيل {updated} مستوى')
    
    @admin.action(description='❌ تعطيل المستويات المحددة')
    def deactivate_levels(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'❌ تم تعطيل {updated} مستوى')


# =========================================================
# إدارة الرغبات
# =========================================================
@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    """
    إدارة رغبات الطلاب
    """
    
    list_display = [
        'get_priority_badge',
        'student_name',
        'student_percentage',
        'get_stream_badge',
        'get_faculty',
        'get_university',
        'created_at',
    ]
    
    list_filter = [
        'student_stream',
        'faculty__university',
        'created_at',
    ]
    
    search_fields = [
        'student_name',
        'faculty__name',
        'faculty__university__name',
    ]
    
    ordering = ['priority']
    
    @admin.display(description='الأولوية')
    def get_priority_badge(self, obj):
        return format_html(
            '<span style="background: #007bff; color: white; padding: 3px 10px; border-radius: 50%; font-weight: bold;">{}</span>',
            obj.priority
        )
    
    @admin.display(description='المساق')
    def get_stream_badge(self, obj):
        colors = {
            'scientific': '#17a2b8',
            'literary': '#6f42c1',
        }
        color = colors.get(obj.student_stream, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 8px; font-size: 0.8em;">{}</span>',
            color,
            obj.get_student_stream_display()
        )
    
    @admin.display(description='الكلية')
    def get_faculty(self, obj):
        return obj.faculty.name
    
    @admin.display(description='الجامعة')
    def get_university(self, obj):
        return obj.faculty.university.name


# =========================================================
# إدارة جلسات التوقع
# =========================================================
class PredictionResultInline(admin.TabularInline):
    """عرض النتائج داخل جلسة التوقع"""
    model = PredictionResult
    extra = 0
    readonly_fields = [
        'priority',
        'faculty',
        'student_percentage',
        'min_percentage',
        'difference',
        'probability_level',
        'created_at',
    ]
    can_delete = False
    max_num = 0
    fk_name = 'session'


@admin.register(PredictionSession)
class PredictionSessionAdmin(admin.ModelAdmin):
    """
    إدارة جلسات التوقع
    """
    
    list_display = [
        'session_code',
        'student_name',
        'student_percentage',
        'get_stream_badge',
        'get_results_count',
        'created_at',
    ]
    
    list_filter = [
        'student_stream',
        'created_at',
    ]
    
    search_fields = [
        'student_name',
        'session_code',
    ]
    
    ordering = ['-created_at']
    
    readonly_fields = ['session_code', 'created_at']
    
    inlines = [PredictionResultInline]
    
    @admin.display(description='المساق')
    def get_stream_badge(self, obj):
        colors = {
            'scientific': '#17a2b8',
            'literary': '#6f42c1',
        }
        color = colors.get(obj.student_stream, '#6c757d')
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 8px; font-size: 0.8em;">{}</span>',
            color,
            obj.get_student_stream_display()
        )
    
    @admin.display(description='عدد الرغبات')
    def get_results_count(self, obj):
        count = obj.results.count()
        return format_html(
            '<span style="background: #28a745; color: white; padding: 3px 10px; border-radius: 10px;">{}</span>',
            count
        )


# =========================================================
# إدارة نتائج التوقع
# =========================================================
@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    """
    إدارة نتائج التوقع
    """
    
    list_display = [
        'get_priority_badge',
        'get_faculty',
        'get_university',
        'student_percentage',
        'min_percentage',
        'get_difference_colored',
        'get_probability_badge',
    ]
    
    list_filter = [
        'probability_level',
        'session__student_stream',
        'faculty__university',
    ]
    
    search_fields = [
        'faculty__name',
        'faculty__university__name',
        'session__student_name',
    ]
    
    ordering = ['-created_at', 'priority']
    
    @admin.display(description='الأولوية')
    def get_priority_badge(self, obj):
        return format_html(
            '<span style="background: #007bff; color: white; padding: 3px 10px; border-radius: 50%; font-weight: bold;">{}</span>',
            obj.priority
        )
    
    @admin.display(description='الكلية')
    def get_faculty(self, obj):
        return obj.faculty.name
    
    @admin.display(description='الجامعة')
    def get_university(self, obj):
        return obj.faculty.university.name
    
    @admin.display(description='الفرق')
    def get_difference_colored(self, obj):
        diff = obj.difference
        if diff > 0:
            color = '#28a745'
            sign = '+'
        elif diff == 0:
            color = '#ffc107'
            sign = ''
        else:
            color = '#dc3545'
            sign = ''
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}{}%</span>',
            color,
            sign,
            f"{diff:.1f}"
        )
    
    @admin.display(description='الاحتمالية')
    def get_probability_badge(self, obj):
        if not obj.probability_level:
            return mark_safe('<span style="color: #999;">—</span>')
        
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            obj.probability_level.color,
            obj.probability_level.name
        )