import logging
import os
import zipfile
from collections import defaultdict
from datetime import datetime
from operator import itemgetter

from django.conf import settings
from django.http.response import HttpResponse
from django.urls import reverse
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from . import serializers

LOG_DIR = os.path.join(settings.BASE_DIR, "logs")
ZIP_DIR = os.path.join(LOG_DIR, "zip")
logger = logging.getLogger(__name__)


class LogView(ListAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.DayLogSerial
    pagination_class = None
    filter_backends = ()

    def get_queryset(self):
        ret = defaultdict(list)
        for name in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, name)
            b = os.path.getsize(file_path)
            if b == 0:
                continue
            m_time = os.path.getmtime(file_path)
            modified_time = datetime.fromtimestamp(m_time)
            day = modified_time.date()
            ret[day].append(dict(
                file_name=name,
                file_size="{:,.0f} KB".format(b/1024),
                modified_time=modified_time,
                preview=reverse("log-preview", kwargs=dict(name=name), request=self.request),
                archive=reverse("log-archive", kwargs=dict(name=name), request=self.request),
            ))
        final_ret = []
        for day in reversed(sorted(ret.keys())):
            log_list = ret[day]
            final_ret.append(dict(
                day=day,
                day_archive=reverse("day-log-archive", kwargs=dict(name=day.strftime("%Y%m%d")),
                                    request=self.request),
                log_list=reversed(sorted(log_list, key=itemgetter("modified_time"))),
            ))
        return final_ret


class LogPreviewView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request, name):
        file_path = os.path.join(LOG_DIR, name)
        if not os.path.exists(file_path):
            raise NotFound()
        b = os.path.getsize(file_path)
        if b > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size is too large")
        with open(file_path, encoding="utf-8") as fo:
            lines = fo.readlines()
            output = lines[:10]
            remaining = len(lines) - 10
            if remaining > 10:
                output += ["."*50] + lines[-10:]
            elif remaining > 0:
                output += lines[-remaining:]
        output = [row.rstrip() for row in output]
        return Response(output)


class BaseArchiveView(APIView):
    permission_classes = (IsAdminUser,)

    def get_file_list(self, name):
        raise NotImplemented()

    def get(self, request, name):
        file_list = self.get_file_list(name)
        if not os.path.exists(ZIP_DIR):
            os.makedirs(ZIP_DIR)
        zip_path = os.path.join(ZIP_DIR, "{}.zip".format(name))
        with zipfile.ZipFile(zip_path, mode="w") as zf:
            for file_path in file_list:
                b = os.path.getsize(file_path)
                if b == 0:
                    continue
                if b > 100 * 1024 * 1024:  # 100 MB
                    raise ValidationError("File size is too large")
                zf.write(file_path, compress_type=zipfile.ZIP_DEFLATED,
                         arcname=os.path.basename(file_path))
        b = os.path.getsize(zip_path)
        ret = dict(
            file_name=zip_path,
            file_size="{:,.0f} KB".format(b/1024),
            file_list=[os.path.basename(file_path) for file_path in file_list],
            download=reverse("zip-download", kwargs=dict(name=name), request=self.request),
        )
        return Response(serializers.ZipSerial(ret).data)


class LogArchiveView(BaseArchiveView):

    def get_file_list(self, name):
        file_path = os.path.join(LOG_DIR, name)
        if not os.path.exists(file_path):
            raise NotFound()
        return [file_path]


class DayLogArchiveView(BaseArchiveView):

    def get_file_list(self, name):
        day = datetime.strptime(name, "%Y%m%d").date()
        day_logs = []
        for file_name in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, file_name)
            m_time = os.path.getmtime(file_path)
            modified_time = datetime.fromtimestamp(m_time)
            if modified_time.date() == day:
                day_logs.append(file_path)
        return day_logs


class ZipDownloadView(APIView):
    """
    WARNING:
    Only download ONE file at the same time to avoid blocking all connection!!!
    """
    permission_classes = (IsAdminUser,)

    def get(self, request, name):
        zip_path = os.path.join(ZIP_DIR, "{}.zip".format(name))
        if not os.path.exists(zip_path):
            raise NotFound()
        b = os.path.getsize(zip_path)
        if b > 10 * 1024 * 1024:  # 100 MB
            raise ValidationError("File size is too large")
        with open(zip_path, "rb") as fo:
            response = HttpResponse(fo.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(zip_path)
            return response
