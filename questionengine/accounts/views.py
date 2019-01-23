from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import RegistrationForm
from django.shortcuts import render, redirect
from chat.models import Conversation, Message

def register(request, conversation_id=None):
    context = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            if conversation_id:
                conversation = Conversation.objects.get(pk=conversation_id)
                conversation.user = user;
                conversation.save()
            else:
                conversation = Conversation()
                conversation.user = user
                conversation.save()
            return redirect('conversation')
    else:
        form = RegistrationForm()
    context['form'] = form
    context['conversation_id'] = conversation_id
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
            try:
                previous_conversation = Conversation.objects.get(user=user)
            except Conversation.DoesNotExist:
                previous_conversation = None
            if conversation_id:
                if previous_conversation:
                    conversation = Conversation.objects.get(pk=conversation_id)
                    for message in Message.objects.filter(conversation=conversation_id):
                        message.conversation = previous_conversation
                        message.save()
                    previous_conversation.save()
                    conversation.delete()
                else:
                    conversation = Conversation()
                    conversation.user = user
                    conversation.save()
            if(next_url):
                return redirect(next_url)
            else:
                return redirect('conversation')
    else:
        form = AuthenticationForm(request.POST)
    context['form'] = form
    context['conversation_id'] = conversation_id
    return render(request, 'login.html', context)
