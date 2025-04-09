from django.urls import path
from . import views
from accounts.views import update_profile, profile  
from .views import PostDeleteView
from .views import PostUpdateView
from .views import PostDetailView

urlpatterns = [
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('update_profile/', update_profile, name='update_profile'),   
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('profile/', profile, name='profile'),   
    path('new/', views.new_post, name='new_post'),
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),  # Detalle del post
    path('post/new/', views.new_post, name='new_post'),  # Crear nuevo post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]

