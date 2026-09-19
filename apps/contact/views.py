import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import ContactMessage


# =========================================================
# الصفحة الرئيسية - نموذج الاتصال
# =========================================================
def index(request):
    """
    صفحة اتصل بنا
    """
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name', '').strip()
            phone_number = request.POST.get('phone_number', '').strip()
            service_type = request.POST.get('service_type', '')
            scope = request.POST.get('scope', 'inquiry')
            message = request.POST.get('message', '').strip()
            
            # ✅ التحقق
            errors = []
            
            if not full_name:
                errors.append('الاسم مطلوب')
            
            if not phone_number:
                errors.append('رقم الهاتف مطلوب')
            
            if not service_type:
                errors.append('نوع الخدمة مطلوب')
            
            if not message or len(message) < 10:
                errors.append('الرسالة يجب أن تكون 10 أحرف على الأقل')
            
            if errors:
                return render(request, 'contact/index.html', {
                    'errors': errors,
                    'form_data': request.POST,
                    'service_types': ContactMessage.SERVICE_CHOICES,
                })
            
            # ✅ حفظ الرسالة
            contact_msg = ContactMessage.objects.create(
                full_name=full_name,
                phone_number=phone_number,
                service_type=service_type,
                scope=scope,
                message=message,
            )
            
            messages.success(
                request,
                f'✅ تم استلام رسالتك بنجاح! رقم الرسالة: {contact_msg.message_code}'
            )
            return redirect('contact:success', code=contact_msg.message_code)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render(request, 'contact/index.html', {
                'errors': [f'حدث خطأ: {str(e)}'],
                'form_data': request.POST,
                'service_types': ContactMessage.SERVICE_CHOICES,
            })
    
    return render(request, 'contact/index.html', {
        'service_types': ContactMessage.SERVICE_CHOICES,
    })


# =========================================================
# صفحة النجاح
# =========================================================
def success(request, code):
    """
    صفحة النجاح بعد إرسال الرسالة
    """
    contact_msg = get_object_or_404(ContactMessage, message_code=code)
    
    # بناء رسالة واتساب
    wa_text = f"""السلام عليكم،
أرسلت رسالة تواصل في منصة سند الطالب:

🎫 رقم الرسالة: {contact_msg.message_code}
👤 الاسم: {contact_msg.full_name}
📱 الهاتف: {contact_msg.phone_number}
📋 الخدمة: {contact_msg.service_display}
🎯 النطاق: {contact_msg.scope_display}

📝 الرسالة:
{contact_msg.message}"""
    
    encoded = urllib.parse.quote(wa_text)
    wa_link = f"https://wa.me/249123456789?text={encoded}"  # ← غيّر الرقم
    
    return render(request, 'contact/success.html', {
        'contact_msg': contact_msg,
        'wa_link': wa_link,
    })