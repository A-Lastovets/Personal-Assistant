from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import BirthdayFilterForm
from dateutil.relativedelta import relativedelta
from django.core.paginator import Paginator


def contacts_home(request):
    """
    Головна сторінка для керування контактами.

    Args:
        request (HttpRequest): Об'єкт запиту.

    Returns:
        HttpResponse: Сторінка для вибору дій з контактами.
    """
    return render(request, 'contacts_app/contact_home.html')


@login_required
def add_contact(request):
    """
    Створення нового контакту.

    Якщо метод POST, створює новий контакт на основі введених даних.
    Якщо метод GET, повертає форму для введення даних.

    Args:
        request (HttpRequest): Об'єкт запиту.

    Returns:
        HttpResponse: Сторінка з формою для додавання контакту.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()

    return render(request, 'contacts_app/add_contact.html', {'form': form})


@login_required
def contact_detail(request, contact_id):
    """
    Показує деталі конкретного контакту.

    Args:
        request (HttpRequest): Об'єкт запиту.
        contact_id (int): Ідентифікатор контакту.

    Returns:
        HttpResponse: Сторінка з деталями контакту.
    """
    contact = get_object_or_404(
        Contact, id=contact_id, user=request.user)
    return render(request, 'contacts_app/contact_detail.html', {'contact': contact})


@login_required
def edit_contact(request, contact_id):
    """
    Редагування існуючого контакту.

    Завантажує контакт за його ідентифікатором і дозволяє змінювати його дані.

    Args:
        request (HttpRequest): Об'єкт запиту.
        contact_id (int): Ідентифікатор контакту.

    Returns:
        HttpResponse: Сторінка з формою для редагування контакту.
    """
    contact = get_object_or_404(
        Contact, id=contact_id, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts_app/edit_contact.html', {
        'form': form,
        'contact': contact
    })


@login_required
def delete_contact(request, contact_id):
    """
    Видалення контакту.

    Завантажує контакт за його ідентифікатором і видаляє його після підтвердження.

    Args:
        request (HttpRequest): Об'єкт запиту.
        contact_id (int): Ідентифікатор контакту.

    Returns:
        HttpResponse: Сторінка підтвердження видалення контакту.
    """
    contact = get_object_or_404(
        Contact, id=contact_id, user=request.user)
    contact.delete()
    return redirect('contact_list')


@login_required
def contact_list(request):
    """
    Виводить список всіх контактів з можливістю пошуку.
    """
    query = request.GET.get('search', '').strip()
    contacts = Contact.objects.filter(
        user=request.user)

    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(contacts, 3)
    page_number = request.GET.get('page')
    contacts_page = paginator.get_page(page_number)

    return render(request, 'contacts_app/contact_list.html', {'contacts': contacts_page})


@login_required
def contact_search(request):
    """
    Пошук контактів за переданим запитом.

    Args:
        request (HttpRequest): Об'єкт запиту з можливим GET параметром 'query'.

    Returns:
        HttpResponse: Сторінка з результатами пошуку контактів або порожнє поле, якщо запиту ще не введено.
    """
    query = request.GET.get(
        'query', '')
    if query:
        contacts = Contact.objects.filter(name__icontains=query)
    else:
        contacts = []

    return render(request, 'contacts_app/contact_search.html', {'contacts': contacts, 'query': query})


@login_required
def upcoming_birthdays(request):
    """
    Отримує контакти з наближаючими днями народження в обраному періоді.

    Args:
        request (HttpRequest): Об'єкт запиту.

    Returns:
        HttpResponse: Сторінка з контактами, що мають наближаючі дні народження.
    """
    today = timezone.localdate()
    period = request.GET.get('period', 1)

    try:
        period = int(period)
    except ValueError:
        period = 1

    end_date = today + relativedelta(months=period)

    all_birthdays = Contact.objects.filter(
        user=request.user)

    results = []
    for contact in all_birthdays:
        contact_birthday_current_year = contact.birthday.replace(
            year=today.year)

        if contact_birthday_current_year < today:
            contact_birthday_next_year = contact.birthday.replace(
                year=today.year + 1)
        else:
            contact_birthday_next_year = contact_birthday_current_year

        if today <= contact_birthday_current_year <= end_date or today <= contact_birthday_next_year <= end_date:

            nearest_birthday = contact_birthday_current_year if contact_birthday_current_year >= today else contact_birthday_next_year
            results.append((contact, nearest_birthday))

    results.sort(key=lambda x: x[1])

    sorted_contacts = [contact for contact, birthday in results]

    form = BirthdayFilterForm(initial={'period': period})

    return render(request, 'contacts_app/upcoming_birthdays.html', {
        'upcoming_birthdays': sorted_contacts,
        'form': form,
    })
