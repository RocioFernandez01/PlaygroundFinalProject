from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def user_profile(request):
    return render(request, 'accounts/profile.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Ajusta según tu configuración de URLs
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def update_profile(request):
    """
    Vista para actualizar el perfil de un usuario.
    """
    if request.method == 'POST':
        # Recibir los formularios con los datos del POST y la instancia del usuario actual
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # Verificar si ambos formularios son válidos
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Guardar los cambios del usuario
            profile_form.save()  # Guardar los cambios del perfil
            return redirect('profile')  # Redirigir al perfil después de guardar
    else:
        # Si no es un POST, se crea el formulario con los datos actuales
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    """
    Vista para mostrar el perfil del usuario.
    """
    profile = request.user.profile  # Obtén el perfil del usuario autenticado
    return render(request, 'accounts/profile.html', {'profile': profile})  # Pasa el perfil a la plantilla

def logout_view(request):
    """
    Cierra la sesión del usuario y lo redirige a la página de inicio de sesión.
    """
    logout(request)
    return redirect("login")

def register(request):
    """
    Vista para registrar un nuevo usuario.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})