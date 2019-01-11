from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Conversation, IceBreaker, Message

def home(request):
    context = {}
    conversation = None

    if request.user.is_authenticated:
        conversation = Conversation.objects.get(user=request.user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            if request.user:
                new_message.conversation = conversation
                new_message.save()
                next_message = Message()
                next_message.text = 'What is ' + new_message.text.translate(None, string.punctuation).split(' ')[-1] + '?'
                next_message.is_user_author = False
                next_message.conversation = conversation
                next_message.save()
            else:
                new_conversation = Conversation()
                new_conversation.save()
                new_message.conversation = new_conversation
                new_message.save()
                return redirect('conversation_id', conversation_id=new_conversation.id)

    form = MessageForm()
    context['form'] = form
    context['conversation'] = conversation
    if conversation:
        context['messages'] = conversation.message_set.all()
    else:
        context['messages'] = [IceBreaker.objects.random(),]
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
