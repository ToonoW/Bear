from django.core.management.base import BaseCommand

from honey import utils
from honey.models import Honeycomb, Honey


class Command(BaseCommand):
    help = '拉取最新节点信息'

    def handle(self, *args, **options):
        for honeycomb in Honeycomb.objects.all():
            Honey.objects.filter(honeycomb=honeycomb).delete()
            honey_configs = utils.honey_info(honeycomb.email, honeycomb.password)
            for config in honey_configs:
                Honey.objects.create(
                    honeycomb=honeycomb,
                    name=config['name'],
                    server=config['server'],
                    server_port=config['server_port'],
                    password=config['password'],
                    load=config['load'],
                    method=config['method'],
                    obfs=config['obfs'],
                    obfs_param=config['obfs_param'],
                    protocol=config['protocol'],
                    protocol_param=config['protocol_param'],
                )
            self.stdout.write('用户 {} 节点拉取成功'.format(honeycomb.email))
        self.stdout.write('更新完成')
