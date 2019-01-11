from django.db import models
from django.contrib.auth.models import User
from random import randint

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class IceBreakerManager(models.Manager):
    def random(self):
        #https://stackoverflow.com/questions/962619/how-to-pull-a-random-record-using-djangos-orm
        count = IceBreaker.objects.all().count()
        random_index = randint(0, count - 1)
        return self.all()[random_index]

class IceBreaker(models.Model):
    text = models.CharField(max_length=2047)
    shown = models.BigIntegerField(default=0)
    swapped = models.BigIntegerField(default=0)
    responded = models.BigIntegerField(default=0)
    objects = IceBreakerManager()

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2047)
    is_user_author = models.BooleanField(default=True)
    is_icebreaker = models.BooleanField(default=False)
    swapped = models.BooleanField(default=False)
    icebreaker = models.ForeignKey(IceBreaker, on_delete=models.PROTECT, null=True, blank=True)

    def __string__():
        return icebreaker;
