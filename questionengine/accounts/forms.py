from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmailSubscription

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ('email',)
        labels = {
                'email': False
                }
        widgets = {
                'email': forms.EmailInput(attrs={'placeholder': 'Type your email'})
                }

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False, help_text='Optional. Enter a valid email address to continue your conversation in email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
