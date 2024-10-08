from django.db import models
from django.core.validators import EmailValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

class Contact(models.Model):
    """
    Модель для зберігання інформації про контакт у книзі контактів.

    Attributes:
        name (str): Ім'я контакту.
        address (str): Адреса контакту.
        phone_number (PhoneNumberField): Номер телефону контакту.
        email (str): Електронна пошта контакту. Перевіряється валідатором EmailValidator.
        birthday (date): День народження контакту.
    """
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField()
    birthday = models.DateField()

    def __str__(self):
        return self.name
    
    def days_until_birthday(self):
        """
        Обчислює кількість днів до наступного дня народження.

        Returns:
            int: Кількість днів до наступного дня народження, або None, якщо день народження не вказано.
        """
        if not self.birthday:
            return None  # Якщо день народження не вказано, повертаємо None

        today = timezone.now().date()  # Отримуємо поточну дату
        next_birthday = self.birthday.replace(year=today.year)  # Призначаємо день народження на поточний рік

        if next_birthday < today:
            next_birthday = self.birthday.replace(year=today.year + 1)  # Якщо день народження вже минув, призначаємо на наступний рік

        return (next_birthday - today).days  # Обчислюємо різницю в днях
