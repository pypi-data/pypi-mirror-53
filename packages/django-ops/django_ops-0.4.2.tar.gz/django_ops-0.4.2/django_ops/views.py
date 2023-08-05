import logging
import os
import platform
import sys
from collections import OrderedDict
from datetime import datetime

import django
import psutil
from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.urls.exceptions import NoReverseMatch

from . import utilities, migration_util

logger = logging.getLogger(__name__)


class RootView(APIView):

    def get(self, request):
        urlconf = __import__("django_ops.urls", {}, {}, [''])
        url_list = []
        for pattern in urlconf.urlpatterns:
            try:
                url = reverse(pattern.name, request=request)
            except NoReverseMatch:
                url = None
            url_list.append(OrderedDict([
                ("name", pattern.name),
                # ("view", pattern.callback.__name__),
                ("url", url),
            ]))
        return Response(url_list)


class PingView(APIView):

    def get(self, request):
        ret = OrderedDict()
        ret["message"] = "ok"
        ret["setting"] = settings.SETTINGS_MODULE
        return Response(ret)


class InfoView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):

        django_info = OrderedDict()
        django_info["debug"] = settings.DEBUG
        django_info["version"] = django.get_version()
        django_info["settings_module"] = settings.SETTINGS_MODULE
        django_info["path"] = ",".join(django.__path__)

        django_info["base_dir"] = settings.BASE_DIR
        # django_info["latest"] = newest(settings.BASE_DIR)

        django_info["start_time"] = utilities.START_TIME
        django_info["start_file_info"] = utilities.START_FILE
        django_info["current_time"] = datetime.now()
        django_info["current_file_info"] = utilities.get_file_info()

        os_info = OrderedDict()
        os_info["platform"] = platform.platform()
        os_info["cpu_count"] = psutil.cpu_count()
        os_info["cpu_count_real"] = psutil.cpu_count(logical=False)
        os_info["ram_total"] = "%.2f GB" % (psutil.virtual_memory().total / 1024 ** 3)
        os_info["ram_used_%"] = psutil.virtual_memory().percent

        python_info = OrderedDict()
        python_info["version"] = sys.version
        python_info["executable"] = sys.executable
        python_info["cwd"] = os.getcwd()
        python_info["command"] = " ".join(sys.argv)
        python_info["pid"] = os.getpid()
        python_info["path"] = sys.path

        resp = OrderedDict([
            ("django", django_info),
            ("os", os_info),
            ("python", python_info),
        ])
        return Response(resp)


class MigrationView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        ret = OrderedDict()
        ret["file"] = migration_util.get_app_migrations()
        ret["db"] = migration_util.get_db_migrations()
        return Response(ret)


class RequestView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        ret = OrderedDict()
        ret["HTTP_HOST"] = request.META.get('HTTP_HOST')
        ret["HTTP_X_FORWARDED_FOR"] = request.META.get('HTTP_X_FORWARDED_FOR')
        ret["HTTP_X_FORWARDED_HOST"] = request.META.get('HTTP_X_FORWARDED_HOST')
        ret["HTTP_X_FORWARDED_SERVER"] = request.META.get('HTTP_X_FORWARDED_SERVER')
        return Response(ret)
