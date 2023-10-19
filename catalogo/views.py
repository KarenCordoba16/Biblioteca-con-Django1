from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>¡Hola mundo!</h1>')

def register(request):
    if request.method == 'GET':
        return render(request, 'registrarion/register.html', {'form': CustomUserCreationForm})
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            login(request, user)

            return redirect('home')
        else:
            return render(request, 'registration/register.html', {"form":form})