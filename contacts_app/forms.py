from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class ContactForm(forms.ModelForm):
    """
    Форма для створення та редагування контактів.

    Використовує модель Contact і включає перевірку номера телефону та електронної пошти.
    """
    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birthday']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'name': 'Ім\'я',
            'address': 'Адреса',
            'phone_number': 'Номер телефону',
            'email': 'Електронна пошта',
            'birthday': 'Дата народження',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Отримуємо користувача з kwargs
        super(ContactForm, self).__init__(*args, **kwargs)

    def clean_phone_number(self):
        """
        Валідація номера телефону. Перевіряє, що номер телефону коректний.

        Returns:
            str: Валідний номер телефону.

        Raises:
            forms.ValidationError: Якщо номер телефону некоректний.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise ValidationError("This field is required.")

        contact_id = self.instance.id  # Використовуємо ID для виключення поточного контакту
        if Contact.objects.filter(user=self.user, phone_number=phone_number).exclude(id=contact_id).exists():
            raise ValidationError("This phone number is already in use by another contact for this user.")
    
        return phone_number

    def clean_email(self):
        """
        Валідація електронної пошти. Перевіряє, що електронна пошта коректна
        та унікальна для поточного користувача.
        """
        email = self.cleaned_data.get('email')

        try:
            EmailValidator()(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")

        contact_id = self.instance.id  # Використовуємо ID для виключення поточного контакту
        if Contact.objects.filter(user=self.user, email=email).exclude(id=contact_id).exists():
            raise ValidationError("This email address is already in use by another contact for this user.")

        return email

class BirthdayFilterForm(forms.Form):
    """
    Форма для вибору періоду для фільтрації контактів з наближаючими днями народження.
    """
    PERIOD_CHOICES = [
        (1, '1 місяць'),
        (3, '3 місяці'),
        (6, '6 місяців'),
        (12, '1 рік'),
    ]

    period = forms.ChoiceField(
        choices=PERIOD_CHOICES, initial=1, label="Виберіть період", widget=forms.Select(attrs={'class': 'form-control'})
    )
