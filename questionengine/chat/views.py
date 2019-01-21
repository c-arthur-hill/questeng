from django.http import HttpResponseNotFound
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .forms import MessageForm
from .models import Conversation, Question, Message, Topic
import re

def different_message(request, message_type, conversation_id=None, question_id=None):
    # acts as home page
    if request.method == 'GET':
        conversation = get_conversation(request.user, conversation_id)
        message = Message()
        form = MessageForm()
        message.is_user_author = False
        if message_type == 'icebreaker':
            # message.set_question()
            if question_id:
                question = Question.objects.get(pk=question_id)
            else:
                question = Question.objects.random()
            if question:
                message.is_question = True
                message.is_icebreaker = True
                message.question = question
                form.initial['last_question'] = question.id
        elif message_type == 'question':
            # message.set_question()
            if conversation:
                last_message = conversation.message_set.last()
                message_text = get_next_message(last_message.text)
                message.text = message_text
                form.initial['last_message'] = message_text
            else:
                last_message = None
        context = {}
        context['different_message'] = message
        context['form'] = form
        if conversation:
            context['conversation_id'] = conversation.id
            # https://stackoverflow.com/questions/20555673/django-query-get-last-n-records
            messages = list(reversed(conversation.message_set.order_by('-id')[:10]))
            if not messages:
                context['empty_messages'] = True
            else:
                messages.pop()
            messages.append(message)
            context['messages'] = messages
        else:
            context['messages'] = [message]
        context['topics'] = Topic.objects.all()
        context['show_save_message'] = True
        return render(request, 'home.html', context)
    else:
        raise PermissionDenied

def new_message(request, conversation_id=None, question_id=None, last_Message=None):
    # displays message history or posts new response
    # user not logged in & answered first icebreaker
    conversation = get_conversation(request.user, conversation_id)
    if request.method == 'GET':
        form = MessageForm()
    elif request.method == 'POST':
        if not conversation:
            # user not logged in, but posted first response
            conversation = Conversation()
            conversation.save()
            conversation_id = conversation.id
        form = MessageForm(request.POST)
        if form.is_valid():
            # shorten this with constructors
            if form.cleaned_data['last_message'] and form.cleaned_data['last_icebreaker']:
                # hacker afoot
                raise PermissionDenied
            elif form.cleaned_data['last_message']:
                last_message = Message()
                last_message.text = form.cleaned_data['last_message']
                last_message.conversation = conversation
                last_message.is_user_author = False
                last_message.save()
            elif form.cleaned_data['last_icebreaker']:
                last_message = Message()
                try:
                    question = Question.objects.get(pk=form.cleaned_data['last_icebreaker'])
                    message.question = question
                    message.conversation = conversation
                    message.is_user_author = False
                    message.save()
                except Question.DoesNotExist:
                    pass
            new_message = form.save(commit=False)
            new_message.conversation = conversation
            new_message.save()
            next_message = Message()
            next_message.text = get_next_message(new_message.text)
            next_message.conversation = conversation
            next_message.is_user_author = False
            next_message.save()
            form = MessageForm()
    else:
        return HttpResponseForbidden()
    
    context = {}
    context['conversation_id'] = conversation_id
    context['form'] = form
    context['messages'] = list(reversed(conversation.message_set.order_by('-id')[:10]))
    context['topics'] = Topic.objects.all()
    context['show_save_message'] = True
    return render(request, 'home.html', context)

def about(request, conversation_id=None):
    context = {}
    context['conversation_id'] = conversation_id
    context['show_save_message'] = True
    return render(request, 'about.html', context)

def get_conversation(request_user, conversation_id):
    #if user is logged in use that convo
    conversation = None
    if conversation_id:
        conversation = Conversation.objects.get(pk=conversation_id)
        if conversation.user and request_user.is_authenticated and conversation.user != request_user:
            raise PermissionDenied
    elif request_user.is_authenticated:
        try:
            conversation = Conversation.objects.get(user=request_user)
        except Conversation.DoesNotExist:
            pass
    return conversation

def get_next_message(current_message):
    return 'What is ' + strip_punctuation(current_message.split(' ')[-1]) + '?'

def strip_punctuation(s):
    return re.sub(r'[^\w\s]', '', s)
