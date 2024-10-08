from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader
import imageio
from io import BytesIO

from .models import File
from .forms import FileUploadForm


from django.views.generic import ListView
from .models import File


from django.views.generic import ListView
from .models import File
from django.core.paginator import Paginator


class FileListView(ListView):
    model = File
    template_name = 'files_app/file_list.html'
    context_object_name = 'files'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-uploaded_at')
        category = self.request.GET.get('category')

        if category == 'all' or not category:
            return queryset

        if category in dict(self.model.CATEGORY_CHOICES).keys():
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        page_obj = paginator.get_page(page_number)

        context['files'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1
        return context


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)

            if file_instance.file.name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                file_instance.category = 'image'
            elif file_instance.file.name.endswith(('.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv')):
                file_instance.category = 'video'
            elif file_instance.file.name.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.csv')):
                file_instance.category = 'document'
            else:
                file_instance.category = 'other'

            try:
                cloudinary_response = cloudinary.uploader.upload(
                    file_instance.file, resource_type='auto')

                file_instance.file = cloudinary_response['secure_url']

                if file_instance.category == 'video':
                    video_url = cloudinary_response['secure_url']

                    reader = imageio.get_reader(video_url)
                    frame = reader.get_data(0)
                    image = BytesIO()
                    imageio.imwrite(image, frame, format='png')
                    image.seek(0)

                    preview_response = cloudinary.uploader.upload(
                        image, resource_type='image')
                    file_instance.preview = preview_response['secure_url']

                file_instance.save()
                return redirect('file_list')
            except Exception as e:
                print(f"Error uploading file: {e}")
                return render(request, 'files_app/upload.html', {'form': form, 'error': str(e)})
    else:
        form = FileUploadForm()

    return render(request, 'files_app/upload.html', {'form': form})
