from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import requests
from io import BytesIO
from django.core.files.base import ContentFile

def fetch_and_save_default_avatar(profile, username):
    """Fetches a default avatar from a URL and saves it to the profile."""
    default_avatar_url = 'https://sudoteam.s3.eu-north-1.amazonaws.com/default_avatar.png'
    
    try:
        response = requests.get(default_avatar_url)
        if response.status_code == 200:
            img = BytesIO(response.content)
            file_name = f'{username}_avatar.png'
            profile.avatar.save(file_name, ContentFile(img.getvalue()), save=False)
            profile.save()
    except requests.RequestException as e:
        print(f"Error fetching avatar from {default_avatar_url}: {e}")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        fetch_and_save_default_avatar(profile, instance.username)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    profile = instance.profile
    if not profile.avatar:
        fetch_and_save_default_avatar(profile, instance.username)
    
    profile.save()
