from django.shortcuts import render


def index(request):
    """
    صفحة المنح الدراسية - قريباً
    """
    return render(request, 'scholarships/index.html')