from django import forms

from blog.models import Blog
from mailing_list.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image' )

