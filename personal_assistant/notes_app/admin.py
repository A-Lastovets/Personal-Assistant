from django.contrib import admin
from .models import Item, Tag, Note
from .forms import NoteForm  # Імпортуємо форму

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    form = NoteForm  # Використовуємо кастомну форму
    list_display = ('title', 'content', 'item', 'created_at')  # Вказуємо, які поля відображати
    search_fields = ('title', 'content')  # Додаємо можливість пошуку
