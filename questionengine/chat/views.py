from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Conversation, Message

def home(request):
    context = {}
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            # if logged in, add the user l8r
            new_conversation = Conversation()
            new_conversation.save()
            new_message.conversation = new_conversation
            new_message.save()
            return redirect('conversation_id', conversation_id=new_conversation.id)

    form = MessageForm()
    messages = Message.objects.all()
    context['form'] = form
    context['messages'] = messages
    return render(request, 'home.html', context)

def conversation(request, conversation_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.conversation = conversation_id
            new_message.save()

    form = MessageForm()
    messages = Message.objects.all()
    context = {}
    context['conversation_id'] = conversation_id
    context['form'] = form
    context['messages'] = messages
    context['not_saved_warning'] = True
    return render(request, 'home.html', context)

def about(request, conversation_id=None):
    context = {}
    context['conversation_id'] = conversation_id
    return render(request, 'about.html', context)
