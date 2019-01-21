from django.contrib import admin
from .models import Conversation, Question, Topic

admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Conversation)
