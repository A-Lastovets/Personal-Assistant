from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag
from .forms import NoteForm
from django.contrib import messages

def note_home(request):
    notes = Note.objects.all()
    return render(request, 'notes_app/note_home.html', {'notes': notes})

def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()

            # Обробка тегів
            tags_str = form.cleaned_data.get('tags')
            if tags_str:
                tags_list = [tag.strip() for tag in tags_str.split(',')]
                for tag_name in tags_list:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    note.tags.add(tag)

            return redirect('note_list')
    else:
        form = NoteForm()

    return render(request, 'notes_app/add_note.html', {'form': form})

def note_list(request):
    query = request.GET.get('q')
    notes = Note.objects.all()

    if query:
        notes = notes.filter(tags__name__icontains=query)  # Фільтрація за тегами

    return render(request, 'notes_app/note_list.html', {'notes': notes})

def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            # Обробка тегів
            tags_data = form.cleaned_data['tags']
            tags = [tag.strip() for tag in tags_data.split(',') if tag.strip()]  # Додано перевірку на непорожні теги
            
            note.tags.clear()  # Очищення існуючих тегів
            for tag in tags:
                # Перевірка, чи тег є валідним рядком
                if tag:
                    tag_obj, created = Tag.objects.get_or_create(name=tag)  # Створення або отримання тегу
                    note.tags.add(tag_obj)  # Додавання тегу до нотатки
            note.save()  # Збереження нотатки
            
            messages.success(request, 'Нотатку успішно оновлено!')
            return redirect('notes_app:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes_app/edit_note.html', {'form': form})

def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        note.delete()
        return redirect('note_list')
    return render(request, 'notes_app/delete_note.html', {'note': note})

def note_list_sorted(request):
    tag = request.GET.get('tag')
    if tag:
        notes = Note.objects.filter(tags__name__icontains=tag)
    else:
        notes = Note.objects.all()
    return render(request, 'notes_app/note_list.html', {'notes': notes})

def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes_app/note_detail.html', {'note': note})
