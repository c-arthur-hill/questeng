from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    last_question = forms.IntegerField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Message
        fields = ['text']
        labels = {
            'text': False
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'full-width', 'autofocus': 'autofocus'})
        }
