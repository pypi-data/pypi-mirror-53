#coding:utf-8

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class AuditLog(models.Model):
    data_e_hora = models.DateTimeField(default=timezone.now, blank=True, null=True)
    atividade = models.CharField(max_length=256)
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=256)
    objeto = models.CharField(max_length=256, default='algum objeto')

    class Meta:
        app_label = 'auditlog'
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-data_e_hora']