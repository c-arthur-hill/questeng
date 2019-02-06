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
from chat.views import new_message, about, create_conversation, create_conversation_from_different_question
from accounts.views import register, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('register/<int:conversation_id>', register, name='register_id'),
    path('login/', login, name='login'),
    path('login/<int:conversation_id>/', login, name='login_id'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', create_conversation, name='home'),
    path('talk/from/<int:question_id>/', create_conversation_from_different_question, name='create_conversation_from_different_question'),
    path('talk/question/<int:question_id>/', new_message, name='conversation'),
    path('talk/<int:conversation_id>/question/<int:question_id>/', new_message, name='conversation_id'),
    path('talk/question/<int:question_id>/topics/', new_message, {'show_topics': True}, name='conversation_topics'),
    path('talk/<int:conversation_id>/question/<int:question_id>/topics/', new_message, {'show_topics': True}, name='conversation_id_topics'),
    path('about/', about, name='about'),    
    path('about/<int:conversation_id>/', about, name='about_id'),
]
