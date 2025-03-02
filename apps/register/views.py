from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method != 'POST':
        form = RegisterForm()
        return render(request, 'register/register.html', {'form': form})

    form = RegisterForm(request.POST)
    
    if not form.is_valid():
        messages.error(request, "Registration failed. Please correct the errors below.")
        return render(request, 'register/register.html', {'form': form})

    username = form.cleaned_data.get('username')
    password1 = form.cleaned_data.get('password1')
    password2 = form.cleaned_data.get('password2')

    if password1 != password2:
        messages.error(request, "Passwords do not match. Please try again.")
        return render(request, 'register/register.html', {'form': form})

    user = form.save()
    user = authenticate(username=username, password=password1)

    if user is None:
        messages.error(request, "Authentication failed. Please try logging in.")
        return render(request, 'register/register.html', {'form': form})

    login(request, user)
    messages.success(request, "You have successfully registered.")
    return redirect('homepage')
