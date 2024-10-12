from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag
from .forms import NoteForm

def note_home(request):
    notes = Note.objects.all()
    return render(request, 'notes_app/note_home.html', {'notes': notes})

def add_note(request):
    tags = Tag.objects.all()  # Отримати всі теги
    if request.method == 'POST':
        form = NoteForm(request.POST)
        new_tag_names = request.POST.getlist('new_tags')  # Отримати нові теги

        if form.is_valid():
            note = form.save()  # Зберегти нотатку

            # Додати нові теги
            for tag_name in new_tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())  # Отримати або створити тег
                note.tags.add(tag)  # Додати тег до нотатки

            return redirect('note_list')

    else:
        form = NoteForm()

    return render(request, 'notes_app/add_note.html', {'form': form, 'tags': tags})

def note_list(request):
    query = request.GET.get('q')
    notes = Note.objects.all()

    if query:
        notes = notes.filter(tags__name__icontains=query)  # Фільтрація за тегами

    return render(request, 'notes_app/note_list.html', {'notes': notes})

def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)  # Отримуємо нотатку за ID
    tags = Tag.objects.all()  # Отримати всі теги
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        new_tag_names = request.POST.getlist('new_tags')  # Отримати нові теги

        if form.is_valid():
            note = form.save()  # Зберегти зміни

            # Оновлення тегів
            note.tags.clear()  # Очистити існуючі теги
            for tag_name in new_tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                note.tags.add(tag)

            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes_app/edit_note.html', {'form': form, 'note': note, 'tags': tags})

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

def delete_tags(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)  # Отримуємо тег за ID

    # Отримуємо ID нотатки з POST-запиту
    note_id = request.POST.get('note_id')

    if request.method == 'POST':
        tag.delete()  # Видаляємо тег
        
        # Перевірка, чи note_id не є None
        if note_id:
            return redirect('edit_note', note_id=note_id)  # Перенаправлення на редагування нотатки
        else:
            return redirect('note_list')  # Або перенаправити на список нотаток, якщо note_id не передано
    
    return render(request, 'notes_app/delete_tags.html', {'tag': tag, 'note_id': note_id})