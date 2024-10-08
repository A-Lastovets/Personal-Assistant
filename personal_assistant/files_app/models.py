from django.db import models
import cloudinary
import cloudinary.uploader
import cloudinary.models


class File(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
    ]

    name = models.CharField(max_length=255)
    file = cloudinary.models.CloudinaryField('file', blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
