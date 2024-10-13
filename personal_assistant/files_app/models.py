from django.db import models
import cloudinary
import cloudinary.uploader
import cloudinary.models
from django.conf import settings


class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    file = cloudinary.models.CloudinaryField('file', blank=False)
    original_extension = models.CharField(max_length=10, blank=True, null=True)
    public_id = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    resource_type = models.CharField(max_length=50, null=True, blank=True)
    preview = cloudinary.models.CloudinaryField(
        'preview', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
