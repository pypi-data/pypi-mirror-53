from rest_framework import serializers

DT_FMT = "%Y/%m/%d %H:%M:%S"


class LogSerial(serializers.Serializer):
    file_name = serializers.CharField()
    file_size = serializers.CharField()
    modified_time = serializers.DateTimeField(format=DT_FMT)
    preview = serializers.URLField()
    archive = serializers.URLField()


class DayLogSerial(serializers.Serializer):
    day = serializers.DateField()
    day_archive = serializers.URLField()
    log_list = LogSerial(many=True)


class DeploySerial(serializers.Serializer):
    name = serializers.CharField()
    load_time = serializers.DateTimeField(format=DT_FMT)
    latest = serializers.JSONField()
    migrations = serializers.JSONField()
    git = serializers.JSONField()


class ZipSerial(serializers.Serializer):
    file_name = serializers.CharField()
    file_size = serializers.CharField()
    file_list = serializers.ListField()
    download = serializers.URLField()
