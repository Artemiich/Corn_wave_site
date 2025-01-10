from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Profile, Track
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class HomeTrack(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'album', 'genre', 'duration', 'audio_file', 'photo' ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'image']

