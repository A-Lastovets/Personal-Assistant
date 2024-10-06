from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """
    Форма для створення та редагування контактів.

    Використовує модель Contact і включає додаткову валідацію номера телефону.
    """

    class Meta:
        model = Contact
        fields = ['name', 'address', 'phone_number', 'email', 'birthday']

    def clean_phone_number(self):
        """
        Валідація номера телефону. Перевіряє, що номер телефону починається з '+'.

        Returns:
            str: Валідний номер телефону.

        Raises:
            forms.ValidationError: Якщо номер телефону не починається з '+'.
        """
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Phone number must include country code and start with '+'.")
        return phone_number
