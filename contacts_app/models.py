from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User


class Contact(models.Model):
    """
    Модель для зберігання інформації про контакт у книзі контактів.

    Attributes:
        user (User): Користувач, якому належить контакт.
        name (str): Ім'я контакту.
        address (str): Адреса контакту.
        phone_number (PhoneNumberField): Номер телефону контакту.
        email (str): Електронна пошта контакту.
        birthday (date): День народження контакту.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=False, blank=False)
    email = models.EmailField()
    birthday = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'phone_number'], name='unique_user_phone_number'),
            models.UniqueConstraint(fields=['user', 'email'], name='unique_user_email'),
        ]

    def __str__(self):
        return self.name

    def days_until_birthday(self):
        """
        Обчислює кількість днів до наступного дня народження.

        Returns:
            int: Кількість днів до наступного дня народження, або None, якщо день народження не вказано.
        """
        if not self.birthday:
            return None

        today = timezone.now().date()
        next_birthday = self.birthday.replace(year=today.year)

        if next_birthday < today:
            next_birthday = self.birthday.replace(year=today.year + 1)

        return (next_birthday - today).days
