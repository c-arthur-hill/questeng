from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    last_message = forms.CharField(required=False, max_length=2047, widget=forms.HiddenInput())
    last_icebreaker = forms.IntegerField(required=False, widget=forms.HiddenInput())
    class Meta:
        model = Message
        fields = ['text']
        labels = {
            'text': False
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'full-width'})
        }
