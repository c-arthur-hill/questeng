from django.shortcuts import render
from .forms import MessageForm
from .models import Message

def home(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.save()
    form = MessageForm()
    messages = Message.objects.all()
    return render(request, 'home.html', {'form': form, 'messages': messages})

def about(request):
    return render(request, 'about.html')
