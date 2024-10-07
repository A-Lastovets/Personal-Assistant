from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file', 'category']
