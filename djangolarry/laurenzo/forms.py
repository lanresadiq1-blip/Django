from django.forms import ModelForm, Form
from django import forms
from laurenzo.models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"