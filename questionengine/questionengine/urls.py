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
from chat.views import different_message, new_message, about
from accounts.views import register, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('register/<int:conversation_id>', register, name='register_id'),
    path('login/', login, name='login'),
    path('login/<int:conversation_id>', login, name='login_id'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', different_message, {'message_type' : 'icebreaker'}, name='home'),
    path('conversation/', new_message, name='conversation'),
    path('conversation/<int:conversation_id>', new_message, name='conversation_id'),
    path('conversation/different/icebreaker/', 
        different_message,
        {'message_type' : 'icebreaker'},
        name='different_icebreaker'),
    path('conversation/different/question/',
        different_message,
        {'message_type': 'question'},
        name='different_question'),
    path('conversation/different/icebreaker/<int:conversation_id>/', 
        different_message,
        {'message_type' : 'icebreaker'},
        name='different_icebreaker_id'),
    path('conversation/different/question/<int:conversation_id>/',
        different_message,
        {'message_type': 'question'},
        name='different_question_id'),
    path('about/', about, name='about'),    
    path('about/<int:conversation_id>', about, name='about_id'),
]
