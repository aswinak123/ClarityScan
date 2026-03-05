from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ClassifyForm(forms.Form):
    text = forms.CharField(
        label='Input Text',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter text for LSTM classification...'}),
    )
