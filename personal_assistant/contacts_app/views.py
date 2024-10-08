from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import BirthdayFilterForm
from dateutil.relativedelta import relativedelta


def contacts_home(request):
    """
    Головна сторінка для керування контактами.
    
    Args:
        request (HttpRequest): Об'єкт запиту.
    
    Returns:
        HttpResponse: Сторінка для вибору дій з контактами.
    """
    return render(request, 'contacts_app/contact_home.html')


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
            form.save()
            return redirect('contact_list')  # Перенаправлення на список контактів
        else:
            # Повертаємо форму з помилками
            return render(request, 'contacts_app/add_contact.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'contacts_app/add_contact.html', {'form': form})


def contact_detail(request, contact_id):
    """
    Показує деталі конкретного контакту.

    Args:
        request (HttpRequest): Об'єкт запиту.
        contact_id (int): Ідентифікатор контакту.

    Returns:
        HttpResponse: Сторінка з деталями контакту.
    """
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'contacts_app/contact_detail.html', {'contact': contact})


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
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Перенаправлення на список контактів
        else:
            # Повертаємо форму з помилками
            print(form.errors)  # Додатковий лог для відстеження проблем
    else:
        form = ContactForm(instance=contact)  # Встановлюємо дані для форми

    return render(request, 'contacts_app/edit_contact.html', {
        'form': form,
        'contact': contact  # Передаємо контакт для шаблону
    })


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
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'contacts_app/delete_contact.html', {'contact': contact})


def contact_list(request):
    """
    Виводить список всіх контактів.

    Також підтримує пошук за ім'ям, адресою, номером телефону або email.

    Args:
        request (HttpRequest): Об'єкт запиту.

    Returns:
        HttpResponse: Сторінка зі списком контактів.
    """
    query = request.GET.get('search', '')
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, 'contacts_app/contact_list.html', {'contacts': contacts})


def contact_search(request):
    """
    Пошук контактів за переданим запитом.

    Args:
        request (HttpRequest): Об'єкт запиту з можливим GET параметром 'query'.

    Returns:
        HttpResponse: Сторінка з результатами пошуку контактів або порожнє поле, якщо запиту ще не введено.
    """
    query = request.GET.get('query')  # Отримати запит із параметрів GET

    if query:
        # Пошук контактів за іменем, що містить запит
        contacts = Contact.objects.filter(name__icontains=query)
    else:
        # Якщо запит не введено, контактів не відображати
        contacts = None

    return render(request, 'contacts_app/contact_search.html', {'contacts': contacts, 'query': query})


def upcoming_birthdays(request):
    """
    Отримує контакти з наближаючими днями народження в обраному періоді.

    Args:
        request (HttpRequest): Об'єкт запиту.

    Returns:
        HttpResponse: Сторінка з контактами, що мають наближаючі дні народження.
    """
    today = timezone.localdate()  # Отримуємо поточну дату
    period = request.GET.get('period', 1)  # За замовчуванням 1 місяць

    try:
        period = int(period)
    except ValueError:
        period = 1  # Якщо період некоректний, то за замовчуванням 1 місяць

    # Обчислюємо кінцеву дату на основі обраного періоду
    end_date = today + relativedelta(months=period)

    print(f'Today: {today}, End date: {end_date}')  # Для перевірки

    # Витягуємо всі контакти
    all_birthdays = Contact.objects.all()

    results = []
    for contact in all_birthdays:
        # Отримуємо день народження в поточному році
        contact_birthday_current_year = contact.birthday.replace(year=today.year)

        # Якщо день народження вже пройшов у цьому році, перевіряємо наступний рік
        if contact_birthday_current_year < today:
            contact_birthday_next_year = contact.birthday.replace(year=today.year + 1)
        else:
            contact_birthday_next_year = contact_birthday_current_year

        # Перевіряємо, чи попадає день народження в обраний період (поточний або наступний рік)
        if today <= contact_birthday_current_year <= end_date or today <= contact_birthday_next_year <= end_date:
            # Додаємо до результатів найближчу дату народження для сортування
            nearest_birthday = contact_birthday_current_year if contact_birthday_current_year >= today else contact_birthday_next_year
            results.append((contact, nearest_birthday))

    # Сортуємо контакти за найближчою датою дня народження
    results.sort(key=lambda x: x[1])

    # Витягуємо відсортованих контактів
    sorted_contacts = [contact for contact, birthday in results]

    print(f'Upcoming birthdays: {len(sorted_contacts)} found')  # Для перевірки

    form = BirthdayFilterForm(initial={'period': period})  # Додаємо вибране значення в форму

    return render(request, 'contacts_app/upcoming_birthdays.html', {
        'upcoming_birthdays': sorted_contacts,  # Передаємо відсортовані контакти
        'form': form,
    })