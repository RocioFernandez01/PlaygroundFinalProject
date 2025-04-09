from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import PostForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied  # Importar PermissionDenied
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import Post, Message
from .models import Message
from django.views.generic import DetailView
from .models import Post

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = 'post'

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"  
    context_object_name = "posts"

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content']  
    template_name = 'blog/edit_post.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.author != self.request.user:
            raise PermissionDenied
        return post
    
    def get_success_url(self):
        return reverse_lazy('post_list')  

    def form_valid(self, form):
        return super().form_valid(form)


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



@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form': form})

def about(request):
    return render(request, 'blog/about.html')

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'blog/inbox.html', {'messages': messages})

@login_required
def home(request):
    posts = Post.objects.all()
    messages = Message.objects.filter(receiver=request.user) if request.user.is_authenticated else []
    return render(request, 'blog/home.html', {'posts': posts, 'messages': messages})

# Vista para la bandeja de entrada (inbox)
@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user)   
    return render(request, 'blog/inbox.html', {'messages': messages})

# Vista para enviar un nuevo mensaje
@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  
            
            if 'receiver' in form.cleaned_data:
                message.receiver = form.cleaned_data['receiver']
            
            message.save()
            return redirect('home')
    else:
        form = MessageForm()

    return render(request, 'blog/send_message.html', {'form': form})

def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if request.user == message.receiver:  # Solo el destinatario puede eliminarlo
        message.delete()

    return redirect('home')

