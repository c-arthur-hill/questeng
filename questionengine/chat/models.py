from django.db import models
from django.contrib.auth.models import User
from random import randint

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class QuestionManager(models.Manager):
    def random(self):
        #https://stackoverflow.com/questions/962619/how-to-pull-a-random-record-using-djangos-orm
        count = Question.objects.all().count()
        if count > 1:
            random_index = randint(0, count - 1)
            return self.all()[random_index]
        else:
            return None

class Topic(models.Model):
    description = models.CharField(max_length=2047)
    responded = models.BigIntegerField(default=0)

    @property
    def top_questions(self):
        return self.question_set.all()[:3]

    def __str__(self):
        return self.description

class Question(models.Model):
    text = models.CharField(max_length=2047)
    shown = models.BigIntegerField(default=0)
    responded = models.BigIntegerField(default=0)
    objects = QuestionManager()
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True, blank=True)
    is_icebreaker = models.BooleanField(default=True)

    @property
    def top_messages(self):
        return self.message_responses_set.all()[:3]

    def __str__(self):
        return self.text        

class Answer(models.Model):
    text = models.CharField(max_length=2047)
    questions = models.ManyToManyField(Question, through='QuestionAnswers')

    def __str__(self):
        return self.text

class QuestionAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    shown = models.BigIntegerField(default=0)
    responded = models.BigIntegerField(default=0)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_user_author = models.BooleanField(default=True)
    is_question = models.BooleanField(default=False)
    is_icebreaker = models.BooleanField(default=False)
    swapped = models.BooleanField(default=False)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, null=True, blank=True)

    def __string__():
        return icebreaker;
