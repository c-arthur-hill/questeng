"""questionengine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from articles.views import about, home, create_article, choose_article_part_type, create_paragraph, create_subheader, create_topic
from accounts.views import register, login

urlpatterns = [
    path('admin', admin.site.urls),
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('about', about, name='about'),
    path('topic/create', create_topic, name='create_topic'),
    path('article/create', create_article, name='create_article'),
    path('article/<int:article_id>/topic/create', create_topic, name='create_topic_id'),
    path('article/<int:article_id>/subheader/create', create_subheader, name='create_subheader'),
    path('article/<int:article_id>/paragraph/create', create_paragraph, name='create_paragraph'),
    path('article/<int:article_id>/part_type/choose', choose_article_part_type, name='choose_article_part_type'),
]
