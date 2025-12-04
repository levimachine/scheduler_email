from django.core.cache import cache

from blog.models import Blog
from scheduler_email import settings


def get_cached_queryset():
    if settings.CACHE_ENABLE:
        key = 'blog_list'
        cached_data = cache.get(key)
        if cached_data is None:
            cached_data = Blog.objects.all()
            cache.set(key, cached_data)
            return cached_data
        return cached_data
    return Blog.objects.all()

