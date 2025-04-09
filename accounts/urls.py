from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register
from django.contrib.auth.views import LoginView, LogoutView
from .views import logout_view
from .views import register_view
from . import views 
from django.urls import path
from .views import user_profile
from django.urls import path
from .views import profile_view 

urlpatterns = [
    path('profile/<str:username>/', profile_view, name='user_profile'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),  # Iniciar sesión
    path('logout/', LogoutView.as_view(), name='logout'),  # Cerrar sesión
    path('register/', register_view, name='register'),  # Registrarse
    
]



