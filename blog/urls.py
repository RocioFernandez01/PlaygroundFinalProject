from django.urls import path
from . import views


urlpatterns = [
    path('about/', views.about, name='about'),
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('new/', views.new_post, name='new_post'),  
    path('post/<int:id>/', views.post_detail, name='post_detail'), 
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
]