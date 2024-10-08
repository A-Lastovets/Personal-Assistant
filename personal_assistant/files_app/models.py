from django.db import models
import cloudinary
import cloudinary.uploader
import cloudinary.models


class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    file = cloudinary.models.CloudinaryField('file', blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    preview = cloudinary.models.CloudinaryField(
        'preview', blank=True, null=True)

    def __str__(self):
        return self.name
