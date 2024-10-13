from django import forms
from .models import Note, Tag


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Теги'
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']
        labels = {
            'title': 'Заголовок',
            'content': 'Описание',
        }
