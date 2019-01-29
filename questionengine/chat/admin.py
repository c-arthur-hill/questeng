from django.contrib import admin
from .models import Conversation, Answer, Question, Topic

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Topic)
admin.site.register(Conversation)
