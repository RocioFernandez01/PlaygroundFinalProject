from django.urls import path
from . import views
from accounts.views import update_profile, profile  
from .views import PostUpdateView, PostDeleteView

urlpatterns = [
    path('update_profile/', update_profile, name='update_profile'),   
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    path('profile/', profile, name='profile'),   
    path('new/', views.new_post, name='new_post'),
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('', views.PostListView.as_view(), name='post_list'),  # Lista de posts
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # Detalle del post
    path('post/new/', views.new_post, name='new_post'),  # Crear nuevo post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),  # Editar post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),  # Eliminar post
]

