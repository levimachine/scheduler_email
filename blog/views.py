from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from blog.services import get_cached_queryset
from blog.forms import BlogForm
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin,UserPassesTestMixin,  CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')
    raise_exception = True

    def test_func(self):
        return self.request.user.has_perm('blog.add_blog')


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog


    def get_queryset(self):
        return get_cached_queryset()



class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        if self.request.user.is_staff:
            return blog
        else:
            blog.views_count += 1
            blog.save()
            return blog
