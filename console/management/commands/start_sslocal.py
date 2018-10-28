import time
import subprocess

from django.core.management.base import BaseCommand, CommandError

from console.models import WorkingQueue
from honey.models import Honey


class Command(BaseCommand):
    help = '用第一个配置快速启动ss-local'

    def pre_check(self):
        honey = Honey.objects.filter(honeycomb__remaining_amount__gt=0).first()
        if honey is None:
            raise CommandError('启动失败，不存在可用节点。')

    def start_work(self, interval):
        honey = WorkingQueue.objects.first()

        cmd = 'python ./shadowsocks/local.py -s {server} -p {server_port} -b 127.0.0.1 -l 1080 -k {password} -m {method} -o {obfs} -t 600'.format(
            server=honey.server,
            server_port=honey.server_port,
            password=honey.password,
            method=honey.method,
            obfs=honey.obfs,
        )
        p = subprocess.Popen(cmd)
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
        WorkingQueue.objects.create(honey=Honey.objects.filter(honeycomb__remaining_amount__gt=0).first())

        self.pre_check()
        self.stdout.write('开始工作')
        self.start_work(5)
        self.stdout.write('结束工作')
