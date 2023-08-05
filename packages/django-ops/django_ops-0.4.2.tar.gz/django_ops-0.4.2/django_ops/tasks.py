import logging
import os

from .models import HouseKeepTask, ArchiveTask

logger = logging.getLogger(__name__)


def execute_housekeep_tasks():
    tasks = HouseKeepTask.objects.filter(enabled=True)
    for task in tasks:
        try:
            logger.info("To run task {} {}".format(task.id, task.task_name))
            task.run()
        except Exception as e:
            logger.error("Failed when running task {} {} {}".format(task.id, task.task_name, e))
        else:
            logger.info("Ran task {} {} successfully".format(task.id, task.task_name))


def execute_archive_tasks():
    tasks = ArchiveTask.objects.filter(enabled=True)
    root = "archived"
    if not os.path.exists(root):
        os.mkdir(root)
    for task in tasks:
        try:
            logger.info("To run task {} {}".format(task.id, task.task_name))
            task.run(root, is_delete=True)
        except Exception as e:
            logger.error("Failed when running task {} {} {}".format(task.id, task.task_name, e))
        else:
            logger.info("Ran task {} {} successfully".format(task.id, task.task_name))
