from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import RegistrationForm
from django.shortcuts import render, redirect

def register(request):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, 'register.html', context)

def login(request, conversation_id=None):
    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            next_url = request.POST.get('next')
            if(next_url):
                return redirect(next_url)
    else:
        form = AuthenticationForm(request.POST)
    context['form'] = form
    return render(request, 'login.html', context)
