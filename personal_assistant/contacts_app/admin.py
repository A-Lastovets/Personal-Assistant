from django.contrib import admin
from .models import Contact  # Імпортуємо модель Contact

@admin.register(Contact)  # Реєструємо модель Contact
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'birthday')  # Вказуємо, які поля відображати в списку
    search_fields = ('name', 'email', 'phone_number')  # Додаємо поле для пошуку
    list_filter = ('birthday',)  # Додаємо фільтр по дню народження
