from django.http import HttpResponseNotFound
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.shortcuts import render, redirect
from .forms import AnswerForm, MessageForm
from .models import Conversation, Question, Answer, QuestionAnswers, Message, Topic
import re

def different_question(request, question_id=1, conversation_id=None):
    # acts as home page
    if request.method == 'GET':
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return HttpResponseNotFound()
        # can return none
        conversation = get_conversation(request.user, conversation_id)
        message = Message()
        form = MessageForm(question_id=question.id)
        message.is_user_author = False
        message.is_question = True
        message.is_icebreaker = question.is_icebreaker
        message.question = question
        context = {}
        context['different_message'] = message
        context['form'] = form
        context['next_question_id'] = question_id + 1
        if conversation:
            context['conversation_id'] = conversation.id
            # https://stackoverflow.com/questions/20555673/django-query-get-last-n-records
            messages = list(reversed(conversation.message_set.order_by('-id')[:5]))
            if not messages:
                context['empty_messages'] = True
            else:
                messages.pop()
            messages.append(message)
            context['messages'] = messages
        else:
            context['messages'] = [message]
            context['empty_messages'] = True
        context['topics'] = Topic.objects.all()
        context['show_save_message'] = True
        return render(request, 'home.html', context)
    else:
        raise PermissionDenied

def new_message(request, conversation_id=None, last_Message=None):
    # displays message history or posts new response
    # user not logged in & answered first icebreaker
    issue_redirect = False
    last_question = None
    conversation = get_conversation(request.user, conversation_id)
    if request.method == 'GET':
        if conversation:
            last_question_message = conversation.last_question()
            if last_question_message:
                last_question = last_question_message.question
        else:
            last_question = None
        form = MessageForm(question_id=last_question.id)
    elif request.method == 'POST':
        if not conversation:
            # user not logged in, but posted first response
            conversation = Conversation()
            conversation.save()
            conversation_id = conversation.id
            issue_redirect = True
        # kind of a hack
        form = MessageForm(request.POST, question_id=request.POST.get('last_question', None))
        if form.is_valid():
            last_question = None
            answer = None
            if form.cleaned_data['last_question']:
                try:
                    last_question = Question.objects.get(pk=form.cleaned_data['last_question'])
                    last_message = Message()
                    last_message.question = last_question
                    last_message.conversation = conversation
                    last_message.is_question = True
                    last_message.is_icebreaker = last_question.is_icebreaker
                    last_message.reponded = True
                    last_message.is_user_author = False
                    last_message.save()
                except Question.DoesNotExist:
                    pass
            else:
                try:
                    last_question = conversation.message_set.last().question
                except Question.DoesNotExist:
                    pass
            if form.cleaned_data['text']:
                answer_form = AnswerForm({'text': form.cleaned_data['text']})
                if answer_form.is_valid():
                    answer = answer_form.save()
                    if last_question:
                        QuestionAnswers.objects.create(question=last_question, answer=answer, responded=1)
                        
                    answer.save()
                else:
                    # I need to return a response here for 
                    # filled out text and chose answer
                    return SuspiciousOperation() 
            else:
                new_message = form.save(commit=False)
                answer = new_message.answer
                new_message.conversation = conversation
                if last_question:
                    question_answer = QuestionAnswers.objects.get(question=last_question, answer=new_message.answer)
                    question_answer.responded = question_answer.responded + 1
                    question_answer.save()
            new_message.save()
            next_message = Message()
            next_question = Question()
            next_question.text = get_next_message(new_message.answer.text)
            next_question.save()
            next_message.question = next_question
            next_message.conversation = conversation
            next_message.is_question = True
            next_message.is_user_author = False
            next_message.save()
            form = MessageForm(question_id=next_question.id)
    else:
        return HttpResponseForbidden()
    if issue_redirect:
        return redirect('conversation_id', conversation_id=conversation_id)
    context = {}
    context['conversation_id'] = conversation_id
    context['form'] = form
    if conversation:
        context['messages'] = list(reversed(conversation.message_set.order_by('-id')[:5]))
    context['topics'] = Topic.objects.all()
    context['show_save_message'] = True
    context['next_question_id'] = 1
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
