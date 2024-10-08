from django.shortcuts import render, redirect, get_object_or_404
from .models import Note 
from .forms import NoteForm

def note_home(request):
    notes = Note.objects.all()
    return render(request, 'notes_app/note_home.html', {'notes': notes})

def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()  # Зберігаємо нотатку разом з тегами
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
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('note_list')
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
