from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post

class SignUpForm(UserCreationForm):
    favorite_team = forms.ChoiceField(
            choices=UserProfile._meta.get_field('favorite_team').choices,
            help_text="Select your favorite team."
        )
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'favorite_team')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {"text"}