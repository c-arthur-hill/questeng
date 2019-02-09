from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)
    total_upvotes = models.IntegerField(default=0)
    total_downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.description

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    last_ordering = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.header

class ArticlePart(models.Model):
    PARAGRAPH = 'p'
    HEADER2 = 'h2'
    HEADER3 = 'h3'
    PART_TYPE_CHOICES = (
        (PARAGRAPH, 'Paragraph'),
        (HEADER2, 'Large Header'),
        (HEADER3, 'Small Header'),
    )
    part_type = models.CharField(max_length=255, choices=PART_TYPE_CHOICES)
    subheader = models.CharField(max_length=255, blank=True)
    paragraph = models.TextField(blank=True)
    ordering = models.IntegerField(default=0)

