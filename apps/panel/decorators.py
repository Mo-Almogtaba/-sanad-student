from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def panel_login_required(view_func):
    """
    يتطلب تسجيل دخول للوصول للوحة
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('panel:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def section_access_required(section_slug):
    """
    يتطلب صلاحية الوصول لقسم معين
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('panel:login')

            # التحقق من الصلاحية
            try:
                profile = request.user.profile
                if not profile.has_section_access(section_slug):
                    messages.error(request, '❌ ليس لديك صلاحية للوصول لهذا القسم')
                    return redirect('panel:dashboard')
            except Exception:
                messages.error(request, '❌ خطأ في الصلاحيات')
                return redirect('panel:dashboard')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def super_admin_required(view_func):
    """
    يتطلب صلاحيات مدير عام
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('panel:login')

        try:
            profile = request.user.profile
            if not profile.is_super_admin:
                messages.error(request, '❌ هذه الصفحة للمدراء فقط')
                return redirect('panel:dashboard')
        except Exception:
            return redirect('panel:dashboard')

        return view_func(request, *args, **kwargs)
    return wrapper
