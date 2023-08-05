import importlib
import logging
from collections import OrderedDict

from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


def import_redis():
    try:
        return importlib.import_module("redis")
    except ModuleNotFoundError:
        raise ValidationError("Redis is not installed")


def get_redis_queue():
    if not hasattr(settings, "CHANNEL_LAYERS"):
        raise ValidationError("No CHANNEL_LAYERS")
    config = settings.CHANNEL_LAYERS["default"]["CONFIG"]
    url = config["hosts"][0]
    prefix = config.get("prefix", "asgi:")
    redis = import_redis()
    connection = redis.StrictRedis.from_url(url)
    return connection, prefix


def get_redis_cache():
    if not hasattr(settings, "CACHES"):
        raise ValidationError("No CACHES")
    caches = settings.CACHES["default"]
    if caches["BACKEND"] == 'redis_cache.RedisCache':
        url = caches['LOCATION'][0]
        redis = import_redis()
        connection = redis.StrictRedis.from_url(url)
        return connection


class RedisGroupView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        connection, prefix = get_redis_queue()
        ret = OrderedDict()
        pattern = "{}:group*".format(prefix)
        keys = sorted(list(connection.keys(pattern)))
        ret["groups"] = [{str(key): connection.zcard(key)} for key in keys]
        return Response(ret)

    def post(self, request):
        connection, prefix = get_redis_queue()
        ret = OrderedDict()
        pattern = "{}:group*".format(prefix)
        keys = sorted(list(connection.keys(pattern)))
        ret["groups"] = [{str(key): connection.zcard(key)} for key in keys]
        ret["removed"] = [{str(key): connection.zremrangebyrank(key, 0, -1)} for key in keys]
        return Response(ret)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def info(request):
    queue_redis, _ = get_redis_queue()
    cache_redis = get_redis_cache()
    ret = OrderedDict()
    ret["QUEUE_SIZE"] = queue_redis.dbsize()
    if cache_redis:
        ret["CACHE_SIZE"] = cache_redis.dbsize()
        v = cache_redis.info()
        ret["REDIS"] = OrderedDict()
        for key in sorted(v):
            # if str(key).startswith("db"):
            ret["REDIS"][key] = v[key]
    return Response(ret)


class FlushCacheView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        cache_redis = get_redis_cache()
        if cache_redis is None:
            raise NotFound()
        ret = OrderedDict()
        ret["total"] = cache_redis.dbsize()
        return Response(ret)

    def post(self, request):
        cache_redis = get_redis_cache()
        if cache_redis is None:
            raise NotFound()
        ret = OrderedDict()
        ret["before"] = cache_redis.dbsize()
        cache_redis.flushdb()
        ret["after"] = cache_redis.dbsize()
        return Response(ret)


class FlushQueueView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queue_redis, _ = get_redis_queue()
        ret = OrderedDict()
        ret["total"] = queue_redis.dbsize()
        ret["http.request"] = queue_redis.llen("asgi:http.request")
        ret["http.disconnect"] = queue_redis.llen("asgi:http.disconnect")
        return Response(ret)

    def post(self, request):
        queue_redis, _ = get_redis_queue()
        ret = OrderedDict()
        ret["before"] = queue_redis.dbsize()
        queue_redis.flushdb()
        ret["after"] = queue_redis.dbsize()
        return Response(ret)
