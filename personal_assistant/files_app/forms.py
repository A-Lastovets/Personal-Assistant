from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file', 'category']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'category']

    def save(self, commit=True):
        file = super().save(commit=False)
        if file.file.name.endswith(('.png', '.jpg', '.jpeg')):
            file.file_type = 'image'
        elif file.file.name.endswith(('.mp4', '.avi')):
            file.file_type = 'video'
        else:
            file.file_type = 'document'
        if commit:
            file.save()
        return file
