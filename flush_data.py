#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.universities.models import University, Faculty, AdmissionRequirement

print("🗑️  حذف البيانات...")
AdmissionRequirement.objects.all().delete()
Faculty.objects.all().delete()
University.objects.all().delete()
print("✅ تم الحذف")

print(f"📊 الإحصائيات بعد الحذف:")
print(f"   الجامعات: {University.objects.count()}")
print(f"   الكليات: {Faculty.objects.count()}")
print(f"   النسب: {AdmissionRequirement.objects.count()}")
