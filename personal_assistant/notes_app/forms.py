from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    tags = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Введіть теги через кому'})
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Якщо ми редагуємо нотатку, відображаємо теги у вигляді списку через кому
        if self.instance and self.instance.pk:  # Перевірка на існування нотатки
            tags_list = self.instance.tags.values_list('name', flat=True)  # Отримуємо лише назви тегів
            self.fields['tags'].initial = ', '.join(tags_list) if tags_list else ''
