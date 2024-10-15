from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import requests
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

# Сигнал для создания профиля
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()

# Сигнал для установки аватара по умолчанию при создании профиля
@receiver(post_save, sender=Profile)
def set_default_avatar(sender, instance, created, **kwargs):
    if created and not instance.avatar:
        # Ссылка на аватар по умолчанию
        default_avatar_url = 'https://sudoteam.s3.eu-north-1.amazonaws.com/default_avatar.png'
        response = requests.get(default_avatar_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue(), 'default_avatar.png')
            instance.avatar.save('default_avatar.png', img_file, save=False)
            instance.save()
