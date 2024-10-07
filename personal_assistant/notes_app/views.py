from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, UserFile
from .forms import NoteForm, UserFileForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# 6. Зберігання нотатків з текстовою інформацією
@login_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})

# 7. Пошук за нотатками
@login_required
def note_list(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(user=request.user).filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__icontains=query))
    else:
        notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

# 8. Редагування та видалення нотатків
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/delete_note.html', {'note': note})

# 9. Додавання  в нотатки "теги"
# (Реалізовано в моделі та формі.)

# 10. СорСортування нотатків за тегами
@login_required
def note_list_sorted(request):
    tag = request.GET.get('tag')
    if tag:
        notes = Note.objects.filter(user=request.user, tags__icontains=tag)
    else:
        notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

# Завантаження файлів
@login_required
def upload_file(request):
    if request.method == "POST":
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user
            user_file.save()
            return redirect('file_list')
    else:
        form = UserFileForm()
    return render(request, 'files/upload_file.html', {'form': form})

@login_required
def file_list(request):
    category = request.GET.get('category', None)
    if category:
        files = UserFile.objects.filter(user=request.user, category=category)
    else:
        files = UserFile.objects.filter(user=request.user)
    return render(request, 'files/file_list.html', {'files': files})
