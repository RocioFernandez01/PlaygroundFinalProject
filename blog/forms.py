from django import forms
from .models import Post
from .models import Message
from .models import Profile
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar'] 

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all(), label="Enviar a")  # Asegurar que se elige un usuario

    class Meta:
        model = Message
        fields = ['receiver', 'content']  # Asegurar que el receptor está en los campos del formulario
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


