from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import requests
from io import BytesIO
from django.core.files.base import ContentFile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        
        # Загрузка аватара по умолчанию с внешнего URL (Amazon S3)
        try:
            default_avatar_url = 'https://sudoteam.s3.eu-north-1.amazonaws.com/default_avatar.png'
            response = requests.get(default_avatar_url, timeout=10)  # Добавляем тайм-аут для запроса

            if response.status_code == 200:
                # Сохраняем изображение, как файл в avatar
                img = BytesIO(response.content)
                file_name = f'{instance.username}_avatar.png'
                profile.avatar.save(file_name, ContentFile(img.getvalue()), save=False)

        except requests.RequestException as e:
            print(f"Error fetching avatar from {default_avatar_url}: {e}")
        
        profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
