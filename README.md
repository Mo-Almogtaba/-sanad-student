# 🎓 سند الطالب — Sanad Student

منصة سودانية متكاملة للخدمات الأكاديمية.

## 🎯 الميزات

- 📝 **التقديم الإلكتروني** للجامعات
- 🎯 **ترتيب الرغبات** وتوقع القبول
- 📜 **الشهادات والتوثيق**
- 🎓 **المنح الدراسية**
- 📖 **دليل التقديم**
- 🔑 **نظام أكواد الوصول**
- 👥 **لوحة تحكم المشرفين**

## 🛠️ التقنيات

- **Backend:** Django 5.x
- **Database:** SQLite (تطوير) / PostgreSQL (إنتاج)
- **Frontend:** Bootstrap 5 + HTML + CSS + JS
- **Static:** WhiteNoise
- **Deploy:** Railway + Cloudflare

## 🚀 التشغيل المحلي

```bash
# 1. استنساخ المستودع
git clone https://github.com/YOUR_USERNAME/sanad-student.git
cd sanad-student

# 2. إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو: venv\Scripts\activate  # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. الهجرات
python manage.py migrate

# 5. إنشاء مستخدم مشرف
python manage.py createsuperuser

# 6. تشغيل الخادم
python manage.py runserver


