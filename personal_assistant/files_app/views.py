from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'files_app/upload.html', {'form': form})


def file_list(request):
    category_filter = request.GET.get('category')
    if category_filter:
        files = File.objects.filter(category=category_filter)
    else:
        files = File.objects.all()

    return render(request, 'files_app/file_list.html', {'files': files})
