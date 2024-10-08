from django.db import models
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True) 
    tags = models.ManyToManyField(Tag, related_name='notes')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
