from django.core.cache import cache

from mailing_list.models import Client, Message
from scheduler_email import settings


def get_cached_queryset(user, model):
    if settings.CACHE_ENABLE:
        if model == Client:
            key = f'client_list_{user.pk}'
        elif model == Message:
            key = f'message_list_{user.pk}'
        else:
            key = f'mailing_list_{user.pk}'
        if user.is_staff:
            cached_data = cache.get(key)
            if cached_data is None:
                cached_data = model.objects.all()
                cache.set(key, cached_data)
                return cached_data
            return cached_data
        else:
            cached_data = cache.get(key)
            if cached_data is None:
                cached_data = model.objects.filter(owner=user)
                cache.set(key, cached_data)
                return cached_data
            return cached_data
    if user.is_staff:
        return model.objects.all()
    return model.objects.filter(owner=user)
