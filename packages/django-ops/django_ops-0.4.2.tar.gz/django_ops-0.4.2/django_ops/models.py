import os
import json
import logging
from datetime import date, datetime, timedelta, time
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

logger = logging.getLogger(__name__)


class BaseSchedule(models.Model):
    class Meta:
        abstract = True

    add_time = models.DateTimeField(auto_now_add=True)
    schedule_time = models.DateTimeField()
    run_time = models.DateTimeField(blank=True, null=True)
    success = models.BooleanField(null=True)
    next_duration = models.DurationField(null=True)


class BaseRecord(models.Model):
    class Meta:
        abstract = True

    add_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(null=True)
    remarks = ArrayField(base_field=models.TextField(), default=list)

    def log(self, msg):
        logger.info(msg)
        self.remarks.append("{} {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))
        self.save(update_fields=["remarks"])

    @property
    def remarks_display(self):
        return "\n".join(self.remarks)


class HouseKeepTask(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    task_name = models.CharField(max_length=50, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    date_field = models.CharField(max_length=50, default="add_time")
    keep_day_count = models.PositiveIntegerField(default=30)
    keep_null = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    batch_size = models.PositiveIntegerField(default=10000)

    def app_label(self):
        if self.content_type:
            return self.content_type.app_label

    def save(self, *args, **kwargs):
        if self.content_type.model_class() is None:
            raise ValueError("Invalid content type")
        return super().save(*args, **kwargs)

    def run(self):
        record = HouseKeepRecord.objects.create(task=self)
        try:
            self.inner_run(record)
        except Exception as e:
            logger.exception("Run task failed")
            record.log(str(e))
            record.success = False
        else:
            record.success = True
        record.save()

    def inner_run(self, record):
        target_model = self.content_type.model_class()  # type: models.Model
        if not self.keep_null:
            kwargs = {
                '{0}__{1}'.format(self.date_field, 'isnull'): True,
            }
            null_sets = target_model.objects.filter(**kwargs)
            null_count = null_sets.count()
            record.log("To delete {} null records".format(null_count))

            while True:
                batch_sets = null_sets[:self.batch_size].values_list("id", flat=True)
                batch_count = len(batch_sets)
                if batch_count == 0:
                    break
                target_model.objects.filter(id__in=batch_sets).delete()
                record.log("Deleted {} null records".format(batch_count))

        if self.keep_day_count >= 3:
            keep_date = date.today() - timedelta(days=self.keep_day_count)
            kwargs = {
                '{0}__{1}'.format(self.date_field, 'lt'): keep_date,
            }
            outdated_sets = target_model.objects.filter(**kwargs)
            outdated_count = outdated_sets.count()
            record.log("To delete {} outdated records".format(outdated_count))
            while True:
                batch_sets = outdated_sets[:self.batch_size].values_list("id", flat=True)
                batch_count = len(batch_sets)
                if batch_count == 0:
                    break
                target_model.objects.filter(id__in=batch_sets).delete()
                record.log("Deleted {} outdated records".format(batch_count))
        else:
            record.log("Keep day count is less than 3!")


class HouseKeepRecord(BaseRecord):
    task = models.ForeignKey(HouseKeepTask, on_delete=models.CASCADE)


class HouseKeepSchedule(BaseSchedule):
    pass


def custom_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, Decimal):
        serial = str(obj)
        return serial
    raise TypeError("Type not serializable {}".format(obj))


class ArchiveTask(models.Model):
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    task_name = models.CharField(max_length=50, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    date_field = models.CharField(max_length=50, default="add_time")

    extra_fields = JSONField(blank=True, help_text='["user__username", "user__profile__ref_user_id"]')
    exclude_fields = JSONField(blank=True, help_text='["play_type_name", "play_radio_name", "try_count"]')
    select_related = JSONField(blank=True, help_text='["user", "user__profile"]')

    keep_day_count = models.PositiveIntegerField(default=30, help_text="value < 30 will be ignored!")
    enabled = models.BooleanField(default=True)

    def app_label(self):
        if self.content_type:
            return self.content_type.app_label

    def run(self, root, is_delete=False):
        record = ArchiveRecord.objects.create(task=self)
        try:
            self.inner_run(root, is_delete)
        except Exception as e:
            logger.exception("Run task failed")
            record.log(str(e))
            record.success = False
        else:
            record.success = True
        record.save()

    def inner_run(self, root, is_delete):
        model_class = self.content_type.model_class()  # type: models.Model
        model_name = self.content_type.name
        if model_class.objects.count() == 0:
            return
        all_fields = set(model_class.objects.values()[0].keys())
        extra_fields = set(self.extra_fields)
        exclude_fields = set(self.exclude_fields)
        select_related = self.select_related
        select_fields = all_fields.union(extra_fields).difference(exclude_fields)
        last_record = model_class.objects.order_by(self.date_field).first()
        if not last_record:
            return
        last_date = getattr(last_record, self.date_field)  # type: datetime
        target_date = datetime.combine(last_date.date(), time.min)
        max_date = datetime.now() - timedelta(days=self.keep_day_count)
        while target_date < max_date:
            target_date_str = target_date.strftime("%Y%m%d")
            logger.info("Archiving for {} on {}".format(model_name, target_date_str))
            start_time = target_date
            end_time = target_date + timedelta(days=1)
            conditions = {
                "{}__gte".format(self.date_field): start_time,
                "{}__lt".format(self.date_field): end_time,
            }
            daily_query = model_class.objects.filter(**conditions)
            daily_count = daily_query.count()
            if daily_count:
                logger.info("To archive {} items".format(daily_count))
                daily_list = list(daily_query.select_related(*select_related).values(*select_fields))
                file_name = "{}_{}.json".format(model_name, target_date_str)
                file_name = os.path.join(root, file_name)
                json.dump(daily_list, open(file_name, "w", encoding="utf-8"),
                          ensure_ascii=False, default=custom_serializer)
                logger.info("Archived {} items".format(daily_count))
                logger.info("Archived for {} on {}".format(model_name, target_date_str))
                if is_delete:
                    daily_query.delete()
                    logger.info("Deleted for {} on {}".format(model_name, target_date_str))
            target_date = target_date + timedelta(days=1)


class ArchiveRecord(BaseRecord):
    task = models.ForeignKey(ArchiveTask, on_delete=models.CASCADE)


class ArchiveSchedule(BaseSchedule):
    pass
