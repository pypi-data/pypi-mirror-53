from django.urls import path

from . import views, redis_views, log_views

urlpatterns = [
    path('', views.RootView.as_view(), name="root"),
    path('ping/',  views.PingView.as_view(), name="ping"),
    path('info/', views.InfoView.as_view(), name="info"),
    path('migration/', views.MigrationView.as_view(), name="migration"),
    path('request/', views.RequestView.as_view(), name="request"),
    # for log
    path('log/', log_views.LogView.as_view(), name="log"),
    path('log/<name>/preview/', log_views.LogPreviewView.as_view(), name="log-preview"),
    path('log/<name>/archive/', log_views.LogArchiveView.as_view(), name="log-archive"),
    path('log/<name>/download/', log_views.ZipDownloadView.as_view(), name="zip-download"),
    path('day-log/<name>/archive/', log_views.DayLogArchiveView.as_view(), name="day-log-archive"),
    # for redis
    path('redis/group/', redis_views.RedisGroupView.as_view(), name="redis-group"),
    path('redis/info/',  redis_views.info, name="redis-info"),
    path('redis/flush-cache/',  redis_views.FlushCacheView.as_view(), name="redis-flush-cache"),
    path('redis/flush-queue/',  redis_views.FlushQueueView.as_view(), name="redis-flush-queue"),
]
