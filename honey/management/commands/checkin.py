from django.core.management.base import BaseCommand

from honey import utils
from honey.models import Honeycomb


class Command(BaseCommand):

    def handle(self, *args, **options):
        for honeycomb in Honeycomb.objects.all():
            msg = utils.honeycomb_checkin(honeycomb.email, honeycomb.password)
            if msg is None:
                self.stdout.write('用户 {} 签到失败'.format(honeycomb.email))
            else:
                self.stdout.write('用户 {} 签到成功。{}'.format(honeycomb.email, msg))
        self.stdout.write('完成签到')