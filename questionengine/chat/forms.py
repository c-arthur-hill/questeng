from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        labels = {
            'text': False
        }
        widgets = {
                'text':  forms.Textarea(attrs={'cols':50, 'rows': 2, 'autofocus': 'autofocus'}),
        }
