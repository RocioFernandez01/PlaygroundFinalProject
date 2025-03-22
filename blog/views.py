from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, Post
from .forms import MessageForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render

def about(request):
    return render(request, 'blog/about.html')

# Vista para actualizar el perfil del usuario
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirigir a la vista del perfil
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'blog/update_profile.html', {'form': form})

# Vista para ver el perfil del usuario
@login_required
def profile(request):
    return render(request, 'blog/profile.html')

# Vista para la página de inicio
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
