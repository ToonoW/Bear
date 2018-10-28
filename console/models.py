from django.db import models

from honey.models import Honey

class WorkingQueue(models.Model):

    class Meta:
        verbose_name = '工作队列'
        verbose_name_plural = '工作队列'

    honey = models.ForeignKey(Honey, on_delete=models.CASCADE)