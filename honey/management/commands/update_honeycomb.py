from django.core.management.base import BaseCommand

from honey import utils
from honey.models import Honeycomb


class Command(BaseCommand):
    help = '更新账号信息'

    def handle(self, *args, **options):
        for honeycomb in Honeycomb.objects.all():
            remaining_count, is_checkin, subscription_url = utils.honeycomb_info(honeycomb.email, honeycomb.password)
            honeycomb.remaining_amount = remaining_count
            honeycomb.is_checkin = is_checkin
            honeycomb.subscription_url = subscription_url
            honeycomb.save()
            self.stdout.write('用户 {} 更新信息'.format(honeycomb.email))
        self.stdout.write('完成更新')