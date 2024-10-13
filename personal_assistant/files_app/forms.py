from django import forms
from .models import File
import os


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

    def save(self, commit=True, user=None):
        file_instance = super().save(commit=False)
        file_instance.user = user
        file_name = file_instance.file.name.lower()
        file_extension = os.path.splitext(file_name)[1]

        if file_extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff']:
            file_instance.category = 'image'
        elif file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv']:
            file_instance.category = 'video'
        elif file_extension in ['.mp3', '.flac', '.wav']:
            file_instance.category = 'audio'
        elif file_extension in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv']:
            file_instance.category = 'document'
        else:
            file_instance.category = 'other'

        file_instance.original_extension = file_extension
        file_instance.name = file_name

        if commit:
            file_instance.save()
        return file_instance
