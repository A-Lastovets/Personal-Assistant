from django.contrib import admin
from .models import Tag, Note
from .forms import NoteForm  # Імпортуємо форму


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    form = NoteForm  # Використовуємо кастомну форму
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title', 'content')  # Додаємо можливість пошуку
