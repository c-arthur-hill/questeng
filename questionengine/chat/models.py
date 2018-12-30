from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    from_ava = models.BooleanField(default=False)
    message = models.CharField(max_length=2047)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return message
