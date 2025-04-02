from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied  # Importar PermissionDenied

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/edit_post.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Verificar si el autor del post es el usuario autenticado
        if post.author != self.request.user:
            raise PermissionDenied  # Lanza un error si el usuario no es el autor
        return post

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')  # Redirigir a la lista de posts después de editar

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Verificar si el autor del post es el usuario autenticado
        if post.author != self.request.user:
            raise PermissionDenied  # Lanza un error si el usuario no es el autor
        return post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

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

def about(request):
    return render(request, 'blog/about.html')

@login_required
def home(request):
    posts = Post.objects.all()  # Obtiene todas las publicaciones
    return render(request, 'blog/home.html', {'posts': posts})

# Vista para ver los detalles de un post
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)  # Obtener el post por su ID
    return render(request, 'blog/post_detail.html', {'post': post})

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
