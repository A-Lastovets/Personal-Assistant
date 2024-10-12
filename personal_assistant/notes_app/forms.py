from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Дозволяємо створення нотаток без тегів
    )
    new_tag = forms.CharField(
        max_length=50,
        required=False,  # Дозволяємо залишити поле порожнім
        label="Додайте новий тег (якщо потрібно):"
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=False)  # Не зберігаємо ще
        if commit:
            instance.save()  # Спочатку зберігаємо нотатку, щоб отримати її id
            
            # Додамо новий тег, якщо він введений
            new_tag = self.cleaned_data.get('new_tag', None)
            if new_tag:
                tag, created = Tag.objects.get_or_create(name=new_tag)
                instance.tags.add(tag)  # Додаємо тег до нотатки

            self.save_m2m()  # Зберігаємо Many-to-Many зв'язки (теги)

        return instance
