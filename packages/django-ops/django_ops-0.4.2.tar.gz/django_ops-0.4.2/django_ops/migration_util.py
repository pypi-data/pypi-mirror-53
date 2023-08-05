import pkgutil
from collections import OrderedDict

from django.conf import settings
from django.db.migrations.recorder import MigrationRecorder


def get_db_migrations():
    ret = []
    records = MigrationRecorder.Migration.objects.order_by('-applied').values(
        "app", "name", "applied"
    )
    apps = list(OrderedDict.fromkeys([x["app"] for x in records]))
    for app in apps:
        related = filter(lambda x: x["app"] == app, records)
        ret.append(OrderedDict([
            ("app", app),
            ("migrations", [OrderedDict([
                ("name", x["name"]),
                ("applied", x["applied"]),
            ]) for x in related]),
        ]))
    return ret


def get_app_migrations():
    ret = []
    apps = settings.INSTALLED_APPS
    for app in apps:
        m = __import__(app, {}, {}, [])
        print(m)
        if not hasattr(m, "migrations"):
            continue
        migration_modules = pkgutil.iter_modules(m.migrations.__path__)
        ret.append(OrderedDict([
            ("app", m.__name__),
            ("migrations", [x[1] for x in migration_modules]),
        ]))
    return ret
