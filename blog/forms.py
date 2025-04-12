from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Team
from django.utils.functional import lazy

def get_all_teams():
    return Team.objects.values_list('id', 'name')

class SignUpForm(UserCreationForm):
    favorite_team = forms.ChoiceField(
            choices=lazy(get_all_teams, list)(),
            widget=forms.Select(attrs={'class': 'form-control'}),
            help_text="Select your favorite team."
        )
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'favorite_team')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'description', 'text')

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {"text"}

class TeamAdminForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'abbreviation', 'sport')