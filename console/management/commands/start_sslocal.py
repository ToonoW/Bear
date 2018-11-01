import time
import subprocess
import json

from django.core.management.base import BaseCommand, CommandError

from console.models import WorkingQueue
from honey.models import Honey, Honeycomb


class Command(BaseCommand):
    help = '用第一个配置快速启动ss-local'

    def pre_check(self):
        honey = Honey.objects.filter(honeycomb__remaining_amount__gt=0).first()
        if honey is None:
            raise CommandError('启动失败，不存在可用节点。')

    def start_work(self, interval):
        honey = WorkingQueue.objects.first().honey

        ss_config = {
            'server': honey.server,
            'server_port': honey.server_port,
            'local_address': '0.0.0.0',
            'local_port': 1080,
            'timeout': 600,
            'workers': 1,
            'password': honey.password,
            'method': honey.method,
            'obfs': honey.obfs,
            'obfs_param': honey.obfs_param,
            'protocol': honey.protocol,
            'protocol_param': honey.protocol_param,
        }
        with open('ss_bear.json', 'w') as f:
            json.dump(ss_config, f, ensure_ascii=True)

        cmd = 'python /app/shadowsocks/local.py -c /app/ss_bear.json'
        p = subprocess.Popen(cmd, shell=True)
        try:
            while True:
                self.stdout.write('工作中')
                if p.poll() is not None:
                    p.terminate()
                    return
                time.sleep(interval)
        except KeyboardInterrupt:
            p.terminate()
            p.wait()

    def handle(self, *args, **options):
        WorkingQueue.objects.all().delete()
        honeycomb = Honeycomb.objects.order_by('-remaining_amount').first()
        WorkingQueue.objects.create(honey=Honey.objects.filter(honeycomb=honeycomb).first())

        self.pre_check()
        self.stdout.write('开始工作')
        self.start_work(5)
        self.stdout.write('结束工作')
