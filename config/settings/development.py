"""
إعدادات التطوير - Development Settings
"""
from .base import *

# ===================== وضع التطوير =====================
DEBUG = True
ALLOWED_HOSTS = ['*']

# ===================== قاعدة البيانات =====================
# استخدام SQLite للتطوير
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===================== البريد الإلكتروني =====================
# طباعة البريد في الطرفية بدلاً من إرساله
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ===================== التطوير =====================
INTERNAL_IPS = ['127.0.0.1']