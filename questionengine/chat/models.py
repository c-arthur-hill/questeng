from django.db import models
from django.contrib.auth.models import User
from random import randint

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def last_question(self):
        return self.message_set.filter(is_question=True).last()

    def last_answer(self):
        return self.message_set.filter(is_question=False).last()

class QuestionManager(models.Manager):
    def random(self):
        #https://stackoverflow.com/questions/962619/how-to-pull-a-random-record-using-djangos-orm
        count = Question.objects.all().count()
        if count > 1:
            random_index = randint(0, count - 1)
            return self.all()[random_index]
        else:
            return None

    def similar(self, question):
        # could use improvements
        # filter previously responded
        # matrix correlate
        return Question.objects.exclude(topic__isnull=True)

class AnswerManager(models.Manager):
    def to_question(self, question):
        return self.filter(questions__in=[question.id]).order_by('-questionanswers')

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
    responded = models.BigIntegerField(default=0)
    skipped = models.BigIntegerField(default=0)
    objects = QuestionManager()
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True, blank=True)
    is_icebreaker = models.BooleanField(default=True)

    def are_top_answers(self):
        return self.answer_set.count() > 0

    def __str__(self):
        return self.text        

class Answer(models.Model):
    text = models.CharField(max_length=2047)
    questions = models.ManyToManyField(Question, through='QuestionAnswers')
    objects = AnswerManager()

    def __str__(self):
        return self.text

class QuestionAnswers(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    skipped = models.BigIntegerField(default=0)
    responded = models.BigIntegerField(default=0)

    class Meta:
        ordering = ('responded',)

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
