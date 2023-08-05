from django.contrib import admin

from auditlog.models import *

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['usuario','atividade','data_e_hora']
    list_filter = [
        'usuario'
    ]
    search_fields = [
        'usuario',
    ]

admin.site.register(AuditLog, AuditLogAdmin)
