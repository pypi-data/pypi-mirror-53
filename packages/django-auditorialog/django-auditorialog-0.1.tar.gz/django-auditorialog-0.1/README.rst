AuditLog
========
AuditLog is a simple django-app for saving logs of activities performed on models.

Quick start
--------------

1. Add `auditlog` to your INSTALLED_APPS setting like this:

`    INSTALLED_APPS = [`
`        ...`
`        'auditlog',` 
`    ]` 

2. Include the auditlog_db database settings:

``DATABASES = {``
`         ...,`
`        'auditlog_db': {`
`        'ENGINE': 'django.db.backends.sqlite3',`
`        'NAME': os.path.join(BASE_DIR, 'auditlog.sqlite3'),`
`        }` 
`    }`

3. Run `python manage.py migrate` to create the auditlog models.

4. To saving log use the piece of code in each view that you want to saving audit:
    `AuditLogDispatcher.send(sender=NotaFiscal, user=request.user, instance=instance, acao='some action')`

5. The `acao` parameter can be:
    1. create
    1. update
    1. delete