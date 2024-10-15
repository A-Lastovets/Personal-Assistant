from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='https://sudoteam.s3.eu-north-1.amazonaws.com/default_avatar.png',
        upload_to='profile_images'
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Проверка существования файла изображения
        try:
            img = Image.open(self.avatar.path)
            if img.height > 250 or img.width > 250:
                new_img = (250, 250)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
        except FileNotFoundError:
            print(f"Файл не знайдено: {self.avatar.path}")
        except ObjectDoesNotExist:
            print("Файл не існує")
        except Exception as e:
            print(f"Помилка обробки зображення: {e}")
