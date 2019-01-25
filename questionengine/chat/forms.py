from django import forms
from .models import Answer, Message

class MessageForm(forms.ModelForm):
    last_question = forms.IntegerField(required=False, widget=forms.HiddenInput())
    text = forms.CharField(label=False, required=False, max_length=240, widget=forms.TextInput(attrs={'class': 'full-width', 'autofocus': 'autofocus'}))
    answer = forms.ModelChoiceField(Answer.objects.all(), label=False, empty_label=None, widget=forms.RadioSelect)
    class Meta:
        model = Message
        fields = ['answer']
        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
