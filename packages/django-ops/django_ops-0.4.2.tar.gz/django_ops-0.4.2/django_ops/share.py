import asyncio
import logging

from django.db import connection
from django.db.utils import InterfaceError

logger = logging.getLogger(__name__)


async def checker():
    while True:
        await asyncio.sleep(5)


class BaseRoutine:
    sleep_at_start = False

    @property
    def interval(self):
        return 60

    @property
    def error_interval(self):
        return 60


class Routine(BaseRoutine):

    def execute(self):
        raise NotImplementedError()

    async def run_forever(self):
        if self.sleep_at_start:
            interval = self.interval
            logger.debug("before executing {}, wait {} seconds".format(self.__class__.__name__, interval))
            await asyncio.sleep(interval)
        while True:
            try:
                logger.debug("start executing {}".format(self.__class__.__name__))
                self.execute()
            except InterfaceError:
                connection.close()
            except Exception as e:
                logger.exception(e)
                error_interval = self.error_interval
                logger.error("error executing {} and wait {} seconds".format(self.__class__.__name__, error_interval))
                await asyncio.sleep(error_interval)
            else:
                interval = self.interval
                logger.debug("end executing {} and wait {} seconds".format(self.__class__.__name__, interval))
                await asyncio.sleep(interval)


class AsyncRoutine(BaseRoutine):

    async def execute(self):
        raise NotImplementedError()

    async def run_forever(self):
        if self.sleep_at_start:
            interval = self.interval
            logger.debug("before executing {}, wait {} seconds".format(self.__class__.__name__, interval))
            await asyncio.sleep(interval)
        while True:
            try:
                logger.debug("start executing {}".format(self.__class__.__name__))
                await self.execute()
            except InterfaceError:
                connection.close()
            except Exception as e:
                logger.exception(e)
                error_interval = self.error_interval
                logger.error("error executing {} and wait {} seconds".format(self.__class__.__name__, error_interval))
                await asyncio.sleep(error_interval)
            else:
                interval = self.interval
                logger.debug("end executing {} and wait {} seconds".format(self.__class__.__name__, interval))
                await asyncio.sleep(interval)
