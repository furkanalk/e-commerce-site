from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import UserCreationForm 
from .forms import kayitolForm
from django.contrib import messages
 
def kayitol(request): 
    if request.method == 'POST':
        form = kayitolForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password == password2:
                user = authenticate(username=username, password=password) 
                login(request, user)
                messages.success(request, ("Basariyla kayit oldunuz."))
                return redirect('anasayfa')
    else:
        form = kayitolForm()
        
    return render(request, 'kayit/kayitol.html', {
        'form':form,
    }) 