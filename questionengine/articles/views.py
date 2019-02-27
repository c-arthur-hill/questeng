from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import ArticleForm, TopicForm, ParagraphForm, SubHeaderForm
from accounts.forms import EmailForm
from .models import Article, Topic

def home(request):
    context = {}
    context['articles'] = Article.objects.all()
    context['success'] = False
    form = None
    if request.method == 'GET':
        form = EmailForm()
    elif request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            context['success'] = True
    else:
        return HttpResponseForbidden()
    context['form'] = form
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def create_article(request):
    context = {}
    form = None
    if request.method == 'GET':
        form = ArticleForm()
    elif request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('choose_article_part_type', article_id=article.id)
    else:
        return HttpResponseForbidden()
    context['header'] = 'Tell Me'
    context['form'] = form
    context['pathname'] = 'create_article'
    context['submit_value'] = 'Next'
    return render(request, 'form.html', context)


def choose_article_part_type(request, article_id):
    context = {}
    article = get_article(request, article_id)
    context['choose_article_part_type'] = True
    context['article'] = article
    return render(request, 'form.html', context)

def create_paragraph(request, article_id):
    context = {}
    article = get_article(request, article_id)
    form = None
    if request.method == 'GET':
        form = ParagraphForm()
    elif request.method == 'POST':
        form = ParagraphForm(request.POST)
        if form.is_valid():
            paragraph = form.save(commit=False)
            article.last_ordering += 1;
            article.save()
            paragraph.ordering = article.last_ordering
            article.save()
            return redirect('choose_article_part_type', article_id=article.id)
    else:
        returnHttpResponseForbidden()
    context['form'] = form
    context['pathname'] = 'create_paragraph'
    context['submit_value'] = 'Save'
    context['article'] = article
    return render(request, 'form.html', context)

def create_subheader(request, article_id):
    context = {}
    article = get_article(request, article_id)
    form = None
    if request.method == 'GET':
        form = SubHeaderForm()
    elif request.method == 'POST':
        form = SubHeaderForm(request.POST)
        if form.is_valid():
            subheader = form.save(commit=False)
            article.last_ordering += 1;
            article.save()
            subheader.ordering = article.last_ordering
            subheader.save()
            return redirect('choose_article_part_type', article_id=article.id)
    else:
        returnHttpResponseForbidden()
    context['form'] = form
    context['pathname'] = 'create_subheader'
    context['submit_value'] = 'Save'
    context['article'] = article
    return render(request, 'form.html', context)

@login_required()
def create_topic(request, article_id=None):
    context = {}
    form = None
    if request.method == 'GET':
        form = TopicForm()
    elif request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            if article_id:
                return redirect('choose_article_part_type', article_id=article_id)
            else:
                return redirect('create_article')
    else:
        returnHttpResponseForbidden()
    context['form'] = form
    if article_id:
        context['pathname'] = 'create_topic_id'
    else:
        context['pathname'] = 'create_topic'
    context['submit_value'] = 'Create'
    return render(request, 'form.html', context)

def get_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        if not article.user == request.user:
            raise HttpResponseNotAllowed()
        else:
            return article
    except Article.DoesNotExist:
        raise HttpResponseNotFound()

def article(request):
    return render(request, 'article.html')
