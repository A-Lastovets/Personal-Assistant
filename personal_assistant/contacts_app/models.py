from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone

class Contact(models.Model):
    """
    Модель для зберігання інформації про контакт у книзі контактів.

    Attributes:
        name (str): Ім'я контакту.
        address (str): Адреса контакту.
        phone_number (str): Номер телефону контакту. Перевіряється за допомогою регулярного виразу.
        email (str): Електронна пошта контакту. Перевіряється валідатором EmailValidator.
        birthday (date): День народження контакту.
    """

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    email = models.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])
    birthday = models.DateField()

    def __str__(self):
        """Повертає рядкове представлення контакту (ім'я)."""
        return self.name

    def days_until_birthday(self):
        """
        Обчислює кількість днів до наступного дня народження.

        Returns:
            int: Кількість днів до наступного дня народження.
        """
        today = timezone.now().date()
        next_birthday = self.birthday.replace(year=today.year)
        if next_birthday < today:
            next_birthday = self.birthday.replace(year=today.year + 1)
        return (next_birthday - today).days
