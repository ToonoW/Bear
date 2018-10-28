from django.db import models


class Honeycomb(models.Model):

    class Meta:
        verbose_name = '蜂巢'
        verbose_name_plural = '蜂巢'

    name = models.CharField('用户名', max_length=64, null=True)
    email = models.CharField('邮箱', max_length=64, unique=True)
    password = models.CharField('密码', max_length=64)
    remaining_amount = models.FloatField('剩余流量', default=0)
    is_checkin = models.BooleanField('签到', default=False)
    last_modify = models.DateTimeField('最后修改', auto_now=True)

    def __str__(self):
        return '{}, {}GB'.format(self.email, self.remaining_amount)


class Honey(models.Model):

    class Meta:
        verbose_name = '蜂蜜'
        verbose_name_plural = '蜂蜜'

    honeycomb = models.ForeignKey(Honeycomb, on_delete=models.CASCADE)
    name = models.CharField('节点名称', max_length=32, default='')
    load = models.IntegerField('负载', default=0)
    server = models.CharField('服务器地址', max_length=64)
    server_port = models.IntegerField('服务器端口')
    password = models.CharField('密码', max_length=64)
    method = models.CharField('算法', max_length=64)
    obfs = models.CharField('混淆', max_length=32, default='')
    obfs_param = models.CharField('混淆参数', max_length=64, default='')
    protocol = models.CharField('协议', max_length=64, default='')
    protocol_param = models.CharField('协议参数', max_length=64, default='')
    ss_version = models.CharField('SS 版本', max_length=16,default='SSR')

    def __str__(self):
        return '{} - {}GB - {}'.format(self.name, self.honeycomb.remaining_amount, self.server)
