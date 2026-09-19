from django.contrib import admin
from django.utils.html import format_html
from .models import (
    GuideSection, GuideCard, GuideListItem,
    GuideLink, GuideImage, GuideVideo, ImportantDate,
)


# ============ Inlines ============
class GuideListItemInline(admin.TabularInline):
    model = GuideListItem
    extra = 1
    fields = ['text', 'icon', 'icon_color', 'order']


class GuideLinkInline(admin.TabularInline):
    model = GuideLink
    extra = 1
    fields = ['title', 'url', 'description', 'icon', 'order']


class GuideImageInline(admin.TabularInline):
    model = GuideImage
    extra = 1
    fields = ['image', 'caption', 'order']


class GuideVideoInline(admin.TabularInline):
    model = GuideVideo
    extra = 1
    fields = ['title', 'youtube_url', 'youtube_id', 'description', 'order']
    readonly_fields = ['youtube_id']


# ============ Admin Classes ============
@admin.register(GuideSection)
class GuideSectionAdmin(admin.ModelAdmin):
    list_display = ['icon_preview', 'title', 'order', 'get_cards_count', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['title']
    search_fields = ['title', 'description']
    list_filter = ['is_active']

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('title', 'description')
        }),
        ('التصميم', {
            'fields': ('icon', 'color')
        }),
        ('الحالة', {
            'fields': ('order', 'is_active')
        }),
    )

    @admin.display(description='🎨')
    def icon_preview(self, obj):
        return format_html(
            '<span style="color: {}; font-size: 1.5em;"><i class="fa {}"></i></span>',
            obj.color, obj.icon
        )

    @admin.display(description='عدد الكروت')
    def get_cards_count(self, obj):
        return obj.cards.count()


@admin.register(GuideCard)
class GuideCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_section', 'card_type', 'order', 'is_open_default', 'is_active']
    list_editable = ['order', 'is_open_default', 'is_active']
    list_display_links = ['title']
    list_filter = ['section', 'card_type', 'is_active']
    search_fields = ['title', 'content']

    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('section', 'card_type', 'title', 'subtitle', 'icon')
        }),
        ('المحتوى', {
            'fields': ('content',),
            'description': 'يدعم HTML بسيط'
        }),
        ('الحالة', {
            'fields': ('order', 'is_open_default', 'is_active')
        }),
    )

    inlines = [
        GuideListItemInline,
        GuideLinkInline,
        GuideImageInline,
        GuideVideoInline,
    ]

    @admin.display(description='القسم')
    def get_section(self, obj):
        return obj.section.title


@admin.register(ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ['icon_preview', 'title', 'date', 'get_status', 'show_countdown', 'order', 'is_active']
    list_editable = ['show_countdown', 'order', 'is_active']
    list_display_links = ['title']
    list_filter = ['is_active', 'show_countdown']
    search_fields = ['title', 'description']

    fieldsets = (
        ('المعلومات', {
            'fields': ('title', 'description', 'date')
        }),
        ('التصميم', {
            'fields': ('icon', 'color')
        }),
        ('الإعدادات', {
            'fields': ('show_countdown', 'order', 'is_active')
        }),
    )

    @admin.display(description='🎨')
    def icon_preview(self, obj):
        return format_html(
            '<span style="color: {}; font-size: 1.5em;"><i class="fa {}"></i></span>',
            obj.color, obj.icon
        )

    @admin.display(description='الحالة')
    def get_status(self, obj):
        if obj.is_past:
            return format_html('<span style="color: #dc3545;">⏰ انتهى</span>')
        elif obj.is_today:
            return format_html('<span style="color: #f59e0b;">🔔 اليوم!</span>')
        else:
            return format_html(
                '<span style="color: #28a745;">⏳ متبقي {} يوم</span>',
                obj.days_remaining
            )


@admin.register(GuideVideo)
class GuideVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'youtube_id', 'get_card', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_display_links = ['title']
    list_filter = ['is_active']
    search_fields = ['title', 'description']

    @admin.display(description='الكرت')
    def get_card(self, obj):
        return obj.card.title if obj.card else '—'