from django import forms
from .models import Note, Tag, Item

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'item', 'tags']  # Додайте поле item

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()  # Заповніть queryset для item
        self.fields['tags'].queryset = Tag.objects.all()  # Заповніть queryset для тегів
