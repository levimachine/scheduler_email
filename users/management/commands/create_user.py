from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='user_verify@mail.ru',
            is_staff=False,
            is_verify=True,
            is_active=True,
            is_superuser=False,
        )
        user.set_password('123')
        user.save()

        user = User.objects.create(
            email='user_not_verify@mail.ru',
            is_staff=False,
            is_verify=False,
            is_active=True,
            is_superuser=False,
            secret_key='1234',
        )
        # Уважаемый проверяющий, чтобы пройти верификацию на сайте нужно ввести секретный ключ 1234
        user.set_password('123')
        user.save()
