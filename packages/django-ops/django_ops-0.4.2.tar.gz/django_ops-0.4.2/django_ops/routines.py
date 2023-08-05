import logging
from datetime import datetime

from . import tasks
from .models import HouseKeepSchedule, ArchiveSchedule
from .share import Routine

logger = logging.getLogger(__name__)


class HouseKeepRoutine(Routine):

    @property
    def interval(self):
        return 60

    def execute(self):
        next_schedule = HouseKeepSchedule.objects.filter(
            success__isnull=True,
            schedule_time__lt=datetime.now()).first()  # type: HouseKeepSchedule
        if next_schedule:
            run_time = datetime.now()
            try:
                tasks.execute_housekeep_tasks()
            except Exception as e:
                logger.exception("Failed schedule {}".format(e))
                next_schedule.success = False
            else:
                next_schedule.success = True
                next_duration = next_schedule.next_duration
                if next_duration:
                    next_time = datetime.now() + next_duration
                    HouseKeepSchedule.objects.create(schedule_time=next_time, next_duration=next_duration)
            finally:
                next_schedule.run_time = run_time
                next_schedule.save()


class ArchiveRoutine(Routine):

    @property
    def interval(self):
        return 60

    def execute(self):
        next_schedule = ArchiveSchedule.objects.filter(
            success__isnull=True,
            schedule_time__lt=datetime.now()).first()  # type: ArchiveSchedule
        if next_schedule:
            run_time = datetime.now()
            try:
                tasks.execute_archive_tasks()
            except Exception as e:
                logger.exception("Failed schedule {}".format(e))
                next_schedule.success = False
            else:
                next_schedule.success = True
                next_duration = next_schedule.next_duration
                if next_duration:
                    next_time = datetime.now() + next_duration
                    ArchiveSchedule.objects.create(schedule_time=next_time, next_duration=next_duration)
            finally:
                next_schedule.run_time = run_time
                next_schedule.save()
