from django.shortcuts import render

def home(request):
    """
    Універсальна головна сторінка для всього проекту.
    
    Повертає базовий шаблон, який містить посилання на різні модулі додатка.
    """
    return render(request, 'base.html')
