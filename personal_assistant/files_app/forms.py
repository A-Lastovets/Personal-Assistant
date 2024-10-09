from django import forms
from .models import File


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

    def save(self, commit=True):
        file_instance = super().save(commit=False)

        file_name = file_instance.file.name.lower()
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            file_instance.category = 'image'
        elif file_name.endswith(('.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv')):
            file_instance.category = 'video'
        elif file_name.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv')):
            file_instance.category = 'document'
        else:
            file_instance.category = 'other'

        if commit:
            file_instance.save()
        return file_instance
