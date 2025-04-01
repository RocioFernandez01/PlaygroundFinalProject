from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, Post
from .forms import MessageForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import ProfileUpdateForm

def about(request):
    return render(request, 'blog/about.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/update_profile.html', {'form': form})

def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def home(request):
    posts = Post.objects.all()  # Obtiene todas las publicaciones
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')  # Cargar los mensajes recibidos
    return render(request, 'blog/home.html', {'posts': posts, 'messages': messages})

# Vista para la bandeja de entrada (inbox)
@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'blog/inbox.html', {'messages': messages})

# Vista para enviar un nuevo mensaje
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # Establecemos el remitente
            message.save()
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = MessageForm()

    return render(request, 'blog/send_message.html', {'form': form})

# Vista para ver los detalles de un post
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)  # Obtener el post por su ID
    return render(request, 'blog/post_detail.html', {'post': post})

# Vista para crear un nuevo post
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) 
            post.author = request.user  # Establecer al autor como el usuario actual
            post.save()  
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = PostForm()  # Formulario vacío

    return render(request, 'blog/new_post.html', {'form': form})
