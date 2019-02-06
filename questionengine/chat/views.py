from django.http import HttpResponseNotFound
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.shortcuts import render, redirect
from django.db.models import F
from .forms import AnswerForm, MessageForm
from .models import Conversation, Question, Answer, QuestionAnswers, Message, Topic
import re
import random

def create_conversation_from_different_question(request, question_id):
    # no conversation, no last_question
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise HttpResponseNotFound
    context = {}
    context['question'] = question
    context['similar'] = Question.objects.similar(question)
    if request.method == 'GET':
        form = MessageForm(question_id=question_id)
    if request.method == 'POST':
        # here question_id should match last_question
        # later on it might be different
        form = MessageForm(request.POST, question_id=question_id)
        if form.is_valid():
            if not form.cleaned_data['text'] and not form.cleaned_data['answer']:
                form.add_error(None, "Say something!")
                context['form'] = form
                return render(request, 'create_conversation_from_different_question.html', context)
            conversation = Conversation()
            if request.user.is_authenticated:
                conversation.user = request.user()
            conversation.save()

            # save question they responded to
            question_message = Message()
            question_message.is_question = True
            question_message.question = question
            question_message.conversation = conversation
            question_message.save()

            # save their answer
            new_message = form.save(commit=False)
            new_message.conversation = conversation

            if form.cleaned_data['text']:
                answer_form = AnswerForm({'text': form.cleaned_data['text']})
                if answer_form.is_valid():
                    answer = answer_form.save()
                    new_message.answer = answer
                else:
                    # need to add validation error to answer 2 long
                    context['form'] = form
                    return render(request, 'talk.html', context)
            elif form.cleaned_data['answer']:
                question_answer = QuestionAnswers.objects.get(question=question, answer=new_message.answer)
                question_answer.responded += 1
                question_answer.save()
            new_message.save()

            # generate next question
            next_question = Question()
            next_question.text = get_next_question(new_message.answer.text)
            next_question.save()
            next_question_message = Message()
            next_question_message.conversation = conversation
            next_question_message.question = next_question
            next_question_message.is_question = True
            next_question_message.save()
            return redirect('conversation_id', conversation_id=conversation.id)
    context['form'] = form
    return render(request, 'create_conversation_from_different_question.html', context)

def create_conversation(request):
    if request.method == 'GET':
        context = {}
        context['form'] = AnswerForm(placeholder='Type something weird')
        context['show_topics'] = False
        context['topics'] = Topic.objects.all()
        context['header'] = 'Talk Weird'
        return render(request, 'home.html', context)
    if request.method == 'POST':
        answer = AnswerForm(request.POST)
        answer = answer.save()
        conversation = Conversation()
        if request.user.is_authenticated:
            conversation.user = request.user
        conversation.save()
        message = Message()
        message.conversation = conversation
        message.is_user_auth = True
        message.answer = answer
        message.save()
        # eventually check fo similar existing questions
        question = Question()
        question.text = get_next_question(answer.text)
        question.conversation = conversation
        question.is_user_auth = False
        question.save()
        next_message = Message()
        next_message.conversation = conversation
        next_message.question = question
        next_message.is_question = True
        next_message.save()
        return redirect('conversation_id', question_id=question.id, conversation_id=conversation.id)

def new_message(request, question_id, conversation_id=None, show_topics=False):
    conversation = get_conversation(request.user, conversation_id)
    if not conversation:
        return redirect(request, 'login')
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise HttpResponseNotFound

    context = {}
    context['conversation_id'] = conversation_id
    if show_topics:
        context['topics'] = Topic.objects.all()
    else:
        context['similar'] = Question.objects.similar(question)
    context['question'] = question

    if request.method == 'GET':
        form = MessageForm(question_id=question.id)
    elif request.method == 'POST':
        form = MessageForm(request.POST, question_id=question.id)
        if form.is_valid():
            # create new message but don't save to return validation errors
            if form.cleaned_data['text']:
                answer_form = AnswerForm({'text': form.cleaned_data['text']})
                if answer_form.is_valid():
                    answer = answer_form.save()
                    new_message = Message()
                    new_message.conversation = conversation
                    new_message.answer = answer
                else:
                    for error in answer_form.errors():
                        form.add_error('text', error)
                    context['form'] = form
                    return render(request, 'talk.html', context) 
            else:
                new_message = form.save(commit=False)
                answer = new_message.answer
                new_message.conversation = conversation
            
            # check if last question was skipped
            last_question_message = conversation.last_question()
            last_question = last_question_message.question
            if last_question == question:
                last_question.responded += 1
            else:
                last_question_message.skipped = True
                last_question.skipped += 1
                try:
                    last_question_answer, created = QuestionAnswers.objects.get_or_create(question=last_question, answer=answer)
                    last_question_answer.skipped += 1
                except QuestionAnswers.DoesNotExist:
                    pass
               
               # save question they just answered as msg
                question_message = Message()
                question_message.conversation = conversation
                question_message.is_question = True
                question_message.question = question
                question_message.save()

            # this was already persisted, it should be an update
            last_question.save() 

            # had to delay for ordering
            new_message.save()

            # updating tracking on new answer to this question
            question_answer, created = QuestionAnswers.objects.get_or_create(question=question, answer=new_message.answer)
            question_answer.responded += 1
            question_answer.save()

            # create and save next question
            # eventually I'll want to check for dupes
            next_question = Question()
            next_question.text = get_next_question(new_message.answer.text)
            next_question.save()
            next_question_message = Message()
            next_question_message.is_question = True
            next_question_message.conversation = conversation
            next_question_message.question = next_question
            next_question_message.save()
            return redirect('conversation_id', question_id=next_question.id, conversation_id=conversation.id)
    else:
        return HttpResponseForbidden()
    
    context['form'] = form
    return render(request, 'talk.html', context)

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

def get_next_question(current_message):
    return 'What is ' + strip_punctuation(current_message.split(' ')[-1]) + '?'

def strip_punctuation(s):
    return re.sub(r'[^\w\s]', '', s)
