from django.core.management.base import BaseCommand

from honey.models import Honey, Honeycomb
from honey import utils


class Command(BaseCommand):
    help = '创建用户和检查可用的节点'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        for index in range(options['count']):
            try:
                name, email, password = utils.honeycomb_create()
            except Exception as e:
                self.stdout.write('从网络创建失败')
            Honeycomb.objects.create(
                name=name,
                email=email,
                password=password,
            )
            self.stdout.write('用户创建成功, email: {}, password: {}'.format(email, password))
        self.stdout.write('创建完成')
