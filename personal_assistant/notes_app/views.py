from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse

from .models import Note, Tag
from .forms import NoteForm


@login_required
def note_home(request):
    # Фильтруем заметки по текущему пользователю
    notes = Note.objects.filter(created_by=request.user)
    return render(request, 'notes_app/note_home.html', {'notes': notes})


@login_required  # Убедитесь, что пользователь авторизован
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)  # Не сохраняем заметку сразу
            note.created_by = request.user  # Устанавливаем текущего пользователя
            note.save()  # Сохраняем заметку

            # Получаем ID всех тегов из формы
            tag_ids = request.POST.getlist('tags')
            for tag_id in tag_ids:
                if tag_id:
                    try:
                        # Получаем тег по ID и текущему пользователю
                        tag = Tag.objects.get(
                            id=tag_id, created_by=request.user)
                        note.tags.add(tag)  # Привязываем тег к заметке
                    except Tag.DoesNotExist:
                        continue  # Игнорируем, если тега нет

            # Обработка нового тега
            new_tag_name = request.POST.get('new_tag')
            if new_tag_name:
                tag, created = Tag.objects.get_or_create(
                    name=new_tag_name.strip(),
                    defaults={'created_by': request.user}
                )
                if created:
                    note.tags.add(tag)  # Привязываем новый тег к заметке

            messages.success(request, 'Заметка успешно добавлена!')
            return redirect('note_list')
    else:
        form = NoteForm()

    # Передаем только теги, созданные текущим пользователем
    user_tags = Tag.objects.filter(created_by=request.user)
    return render(request, 'notes_app/add_note.html', {'form': form, 'tags': user_tags})


@login_required
def note_list(request):
    query = request.GET.get('q')
    tag_query = request.GET.get('tag')  # Додати параметр для пошуку за тегами
    # Фільтруємо нотатки за поточним користувачем
    notes = Note.objects.filter(created_by=request.user)

    if query:
        # Фільтруємо за заголовком або тегами
        notes = notes.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    if tag_query:
        notes = notes.filter(tags__name__icontains=tag_query).distinct()

    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notes_app/note_list.html', {'page_obj': page_obj, 'query': query, 'tag_query': tag_query})


@login_required
def edit_note(request, note_id):
    # Фильтруем заметки по текущему пользователю
    note = get_object_or_404(Note, id=note_id, created_by=request.user)
    if request.method == "POST":
        # Передаем текущую заметку в форму
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)  # Сохраняем изменения, но не сразу
            note.created_by = request.user  # Устанавливаем текущего пользователя
            note.save()  # Сохраняем заметку

            # Очищаем предыдущие теги и добавляем новые
            note.tags.clear()  # Удаляем все текущие теги
            tag_ids = request.POST.getlist('tags')
            for tag_id in tag_ids:
                if tag_id:
                    try:
                        tag = Tag.objects.get(
                            id=tag_id, created_by=request.user)
                        note.tags.add(tag)  # Привязываем тег к заметке
                    except Tag.DoesNotExist:
                        continue  # Игнорируем, если тега нет

            # Обработка нового тега
            new_tag_name = request.POST.get('new_tag')
            if new_tag_name:
                tag, created = Tag.objects.get_or_create(
                    name=new_tag_name.strip(),
                    defaults={'created_by': request.user}
                )
                if created:
                    note.tags.add(tag)  # Привязываем новый тег к заметке

            messages.success(request, 'Заметка успешно обновлена!')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)

    # Передаем только теги, созданные текущим пользователем
    user_tags = Tag.objects.filter(created_by=request.user)
    return render(request, 'notes_app/edit_note.html', {'form': form, 'note': note, 'tags': user_tags})


@login_required
def delete_note(request, note_id):
    # Фильтруем заметки по текущему пользователю
    note = get_object_or_404(Note, id=note_id, created_by=request.user)
    note.delete()
    messages.success(request, 'Заметка успешно удалена!')
    return redirect('note_list')


@login_required
def note_list_sorted(request):
    tag = request.GET.get('tag')
    if tag:
        # Фильтруем заметки по текущему пользователю
        notes = Note.objects.filter(
            tags__name__icontains=tag, created_by=request.user)
    else:
        # Фильтруем заметки по текущему пользователю
        notes = Note.objects.filter(created_by=request.user)
    return render(request, 'notes_app/note_list.html', {'notes': notes})


@login_required
def note_detail(request, note_id):
    # Фильтруем заметки по текущему пользователю
    note = get_object_or_404(Note, id=note_id, created_by=request.user)
    return render(request, 'notes_app/note_detail.html', {'note': note})


@login_required
def add_tag(request):
    if request.method == "POST":
        tag_name = request.POST.get('name')
        if tag_name:
            tag, created = Tag.objects.get_or_create(
                name=tag_name.strip(),
                # Устанавливаем создателя тега
                defaults={'created_by': request.user}
            )
            if created:
                messages.success(request, 'Тег успешно добавлен!')
            else:
                messages.warning(request, 'Тег уже существует!')
    return redirect('add_note')
