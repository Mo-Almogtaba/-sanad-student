import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

print("=" * 50)
print("STATIC_URL:", settings.STATIC_URL)
print("STATIC_ROOT:", settings.STATIC_ROOT)
print("STORAGE:", getattr(settings, 'STATICFILES_STORAGE', 'N/A'))
print("MIDDLEWARE WhiteNoise:", 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE)
print("DEBUG:", settings.DEBUG)
print("=" * 50)
