from django.core.management.base import BaseCommand, CommandError

from honey.models import Honey


class Command(BaseCommand):
    help = '用第一个配置快速启动ss-local'

    def handle(self, *args, **options):
        honey = Honey.objects.filter(honeycomb__remaining_amount__gt=0).first()
        if honey is None:
            raise CommandError('启动失败，不存在可用节点。')
