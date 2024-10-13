import cloudinary.exceptions
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect

import cloudinary
import cloudinary.uploader

import imageio
from io import BytesIO

import mimetypes

import requests
import os

from .models import File
from .forms import FileUploadForm

import cloudinary.api


class FileListView(ListView):
    model = File
    template_name = 'files_app/file_list.html'
    context_object_name = 'files'
    paginate_by = 5

    def get_queryset(self):
        # Ограничиваем выборку файлами текущего пользователя
        queryset = super().get_queryset().filter(
            user=self.request.user).order_by('-uploaded_at')
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
            file_instance = form.save(commit=False, user=request.user)

            if file_instance.category == 'image':
                resource_type = 'image'
            elif file_instance.category in ['video', 'audio']:
                resource_type = 'video'
            else:
                resource_type = 'raw'

            try:
                cloudinary_response = cloudinary.uploader.upload(
                    file_instance.file,
                    resource_type=resource_type,
                    access_mode='public'
                )

                file_instance.file = cloudinary_response['secure_url']
                file_instance.public_id = cloudinary_response['public_id']
                file_instance.resource_type = cloudinary_response['resource_type']

                if file_instance.category == 'video':
                    video_url = cloudinary_response['secure_url']
                    reader = imageio.get_reader(video_url)
                    frame = reader.get_data(0)
                    image = BytesIO()
                    imageio.imwrite(image, frame, format='png')
                    image.seek(0)

                    preview_response = cloudinary.uploader.upload(
                        image, resource_type='image'
                    )

                    file_instance.preview = preview_response['secure_url']

                file_instance.save()
                return redirect('file_list')
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")
                return render(request, 'files_app/upload.html', {'form': form, 'error': str(e)})
    else:
        form = FileUploadForm()

    return render(request, 'files_app/upload.html', {'form': form})


def download_file(request, file_id):

    file_instance = get_object_or_404(File, id=file_id)

    file_url = str(file_instance.file)

    if not file_url.endswith(file_instance.original_extension):
        file_url += file_instance.original_extension

    print(f"URL для скачивания: '{file_url}'")

    try:
        response = requests.get(file_url)
        response.raise_for_status()

        file_name = file_instance.name
        file_extension = file_instance.original_extension or ''

        content_type, _ = mimetypes.guess_type(file_name + file_extension)
        if content_type is None:
            content_type = 'application/octet-stream'

        file_name, file_extension = os.path.splitext(file_instance.name)

        file_extension = file_instance.original_extension or file_extension

        download_response = HttpResponse(response.content)
        download_response['Content-Disposition'] = f'attachment; filename="{
            file_name}{file_extension}"'
        download_response['Content-Type'] = content_type

        return download_response

    except requests.HTTPError as e:
        print(f"Ошибка HTTP: {e.response.status_code}")
        return HttpResponse(f"Ошибка: не удалось скачать файл. Код ошибки: {e.response.status_code}", status=500)
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return HttpResponse(f"Ошибка: {str(e)}", status=500)


def delete_file(request, file_id):

    file_instance = get_object_or_404(File, id=file_id)
    public_id = file_instance.public_id
    resource_type = file_instance.resource_type

    try:
        response = cloudinary.uploader.destroy(
            public_id, resource_type=resource_type, invalidate=True)
        print(f"Ответ от Cloudinary: {response}")

        if response.get('result') == 'ok' or response.get('result') == 'deleted':

            file_instance.delete()
            return redirect('file_list')
        else:
            print(f"Файл не найден или не был удалён. Ответ: {response}")
            return HttpResponse("Ошибка: файл не найден или не был удалён.", status=404)

    except cloudinary.exceptions.Error as e:
        return HttpResponse("Ошибка: не удалось получить информацию о файле.", status=500)
    except Exception as e:
        print(f"Ошибка при удалении файла из Cloudinary: {str(e)}")
        return HttpResponse("Ошибка: не удалось удалить файл.", status=500)
