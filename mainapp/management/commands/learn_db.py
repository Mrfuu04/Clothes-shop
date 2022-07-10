from django.core.management.base import BaseCommand
from django.db.models import Q, F, Case, When, CharField, Value

from authapp.models import User
from mainapp.models import Products


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_products = Products.objects.filter(
            Q(name='Синяя куртка The North Face') | Q(category__name='Обувь') | Q(price__gt=100000)
        )

        admin_name = Value('Админ')
        not_admin_name = Value('Пользователь')

        action_admin_1 = When(Q(is_superuser=True), then=admin_name)
        action_admin_2 = When(Q(is_superuser=False), then=not_admin_name)

        test = User.objects.annotate(
            is_admin=Case(
                action_admin_1,
                action_admin_2,
                output_field=CharField()
            )
        )

        for user in test:
            print(f'Пользователь {user} является {user.is_admin}')
