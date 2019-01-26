from django import forms
from .models import Answer, Message

class MessageForm(forms.ModelForm):
    last_question = forms.IntegerField(required=False, widget=forms.HiddenInput())
    text = forms.CharField(label=False, required=False, max_length=240, widget=forms.TextInput(attrs={'class': 'full-width', 'autofocus': 'autofocus'}))
    answer = forms.ModelChoiceField(None, label=False, empty_label='Other', widget=forms.RadioSelect)
    class Meta:
        model = Message
        fields = ['answer']

    def __init__(self, *args, **kwargs):
        last_question = kwargs.pop('last_question', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset=last_question.top_answers
        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
