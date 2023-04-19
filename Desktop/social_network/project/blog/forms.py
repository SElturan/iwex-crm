from django import forms

from .models import *
from django.core.validators import MinValueValidator, MaxValueValidator


class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(500)
        ]
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'content', 'image', )
