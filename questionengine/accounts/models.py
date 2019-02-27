from django.db import models

class EmailSubscription(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
