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
