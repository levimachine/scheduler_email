from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='content_manager@mail.ru',
            is_superuser=False,
            is_staff=True,
            is_active=True,
            is_verify=True,
        )
        user.set_password('123')
        permission = Permission.objects.get(codename='add_blog')
        group = Group.objects.create(name='Content manager')
        group.permissions.add(permission)
        user.groups.add(group)
        user.save()
