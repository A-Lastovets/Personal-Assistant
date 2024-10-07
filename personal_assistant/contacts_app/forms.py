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

        # PhoneNumberField вже забезпечує валідацію номера телефону,
        # тому додаткова перевірка не потрібна.
        return phone_number  # Повертаємо номер у форматі, який ви хочете

    def clean_email(self):
        """
        Валідація електронної пошти. Перевіряє, що електронна пошта коректна
        та унікальна в базі даних.
        """
        email = self.cleaned_data.get('email')
        try:
            EmailValidator()(email)
        except ValidationError:
            raise ValidationError("Enter a valid email address.")

        # Перевірка унікальності електронної адреси
        if Contact.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")

        return email