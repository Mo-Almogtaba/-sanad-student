#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import Section


sections_data = [
    {'name': 'التقديم الإلكتروني', 'slug': 'applications', 'icon': 'fa-file-alt', 'order': 1},
    {'name': 'الشهادات والتوثيق', 'slug': 'certificates', 'icon': 'fa-certificate', 'order': 2},
    {'name': 'اتصل بنا', 'slug': 'contact', 'icon': 'fa-envelope', 'order': 3},
    {'name': 'أكواد الوصول', 'slug': 'access', 'icon': 'fa-key', 'order': 4},
    {'name': 'بيانات الجامعات', 'slug': 'data_entry', 'icon': 'fa-database', 'order': 5},
    {'name': 'الإعلانات', 'slug': 'announcements', 'icon': 'fa-bullhorn', 'order': 6},
    {'name': 'دليل التقديم', 'slug': 'guide', 'icon': 'fa-book-open', 'order': 7},
]

print()
print("=" * 60)
print("  📋 إنشاء الأقسام")
print("=" * 60)

created_count = 0
for data in sections_data:
    section, created = Section.objects.get_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        created_count += 1
        print(f"  ✅ {section.name}")
    else:
        print(f"  ⏭️  {section.name}")

print()
print(f"  ✅ تم إنشاء {created_count} قسم")
print(f"  📊 الإجمالي: {Section.objects.count()}")
print("=" * 60)
print()

