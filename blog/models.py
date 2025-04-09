from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog_profile')
    bio = models.TextField(blank=True)   
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) 

    def __str__(self):
        return f'{self.user.username} Profile'

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # Para marcar si el mensaje fue leído o no

    def __str__(self):
        return f"Mensaje de {self.sender.username} a {self.receiver.username}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
