import django.forms as forms
from .models import Article, ArticlePart, Topic

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['topic', 'header']
        labels = {
                'header': 'Article title'
                }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['description']

class SubHeaderForm(forms.ModelForm):
    class Meta:
        model = ArticlePart
        fields = ['subheader']

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = ArticlePart
        fields = ['paragraph']

