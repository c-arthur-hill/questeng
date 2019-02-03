from django import forms
from .models import Answer, Question, Message

class MessageForm(forms.ModelForm):
    last_question = forms.IntegerField(required=False, widget=forms.HiddenInput())
    text = forms.CharField(label=False, required=False, max_length=240, widget=forms.TextInput(attrs={'class': 'full-width', 'autofocus': 'autofocus'}))
    answer = forms.ModelChoiceField(None, label=False, empty_label='Other', widget=forms.RadioSelect)
    class Meta:
        model = Message
        fields = ['answer']

    def __init__(self, *args, **kwargs):
        # clean in view and pass in
        question_id = kwargs.pop('question_id', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['last_question'].initial=question_id
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return
        if question.are_top_answers():
            # might want to pass in user in future
            self.fields['answer'].queryset=Answer.objects.to_question(question)
        else:
            self.fields['answer'].queryset=Answer.objects.none()
            self.fields['answer'].widget=forms.HiddenInput()
            self.fields['answer'].required=False
            self.fields['text'].required=True
        

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop('placeholder', False)
        super(AnswerForm, self).__init__(*args, **kwargs)
        if placeholder:
            self.fields['text'].widget = forms.TextInput(attrs={'placeholder': placeholder, 'class': 'full-width', 'autofocus': 'autofocus'})
