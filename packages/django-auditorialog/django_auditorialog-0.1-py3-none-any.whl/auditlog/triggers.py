#coding: utf-8

import django.dispatch
from auditlog.models import AuditLog

import traceback
import sys

def registra_log(sender, **kwargs):
	try:
		instance = kwargs['instance']
		user = kwargs['user']
		acao = kwargs['acao']
		if instance is not None:
			if acao == 'create':
				atividade = f'Criou o objeto: {instance.__class__}: pk: {instance.pk}'
			elif acao == 'update':
				atividade = f'Alterou o objeto {instance.__class__}|Propriedades: {instance.__dict__}'
			elif acao == 'delete':
				atividade = f'Deletou o objeto {instance.__class__}: pk: {instance.pk}'
			AuditLog.objects.create(usuario=user.username, atividade=atividade, objeto=instance.__class__)
		else:
			print('AuditLog Error: Vc precisa indicar a instância da classe para o AuditLog')
	except:
		print("Error no AuditLog")
		traceback.print_exc(file=sys.stdout)

AuditLogDispatcher = django.dispatch.Signal(providing_args=['user','instance','acao'])
AuditLogDispatcher.connect(registra_log)
