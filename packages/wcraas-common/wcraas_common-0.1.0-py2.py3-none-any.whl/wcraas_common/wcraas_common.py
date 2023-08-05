# -*- coding: utf-8 -*-

"""The WCraaS Common module aims to single-source reused code across WCraaS the platform."""

import logging
import aio_pika

from aio_pika import connect_robust
from aio_pika.pool import Pool

from wcraas_common.config import AMQPConfig


__all__ = ("WcraasWorker",)


class WcraasWorker:
    """
    Base class for WCraaS Worker classes, aiming to single-source AMQP boilerplate.
    """

    def __init__(self, amqp: AMQPConfig, loglevel: int, *args, **kwargs):
        self.amqp = amqp
        self.logger = logging.getLogger("wcraas.common")
        self.logger.setLevel(loglevel)
        self.loglevel = loglevel
        self._amqp_pool = self.create_channel_pool()

    def create_channel_pool(self, pool_size: int = 2, channel_size: int = 10) -> Pool:
        """
        Given the max connection pool size and the max channel size create a channel Pool.

        :param pool_size: Max size for the underlying connection Pool.
        :type pool_size: integer
        :param channel_size: Max size for the channel Pool.
        :type channel_size: integer
        """

        async def get_connection():
            return await connect_robust(
                host=self.amqp.host,
                port=self.amqp.port,
                login=self.amqp.user,
                password=self.amqp.password,
            )

        connection_pool = Pool(get_connection, max_size=pool_size)

        async def get_channel() -> aio_pika.Channel:
            async with connection_pool.acquire() as connection:
                return await connection.channel()

        return Pool(get_channel, max_size=channel_size)

    def __repr__(self):
        return f"{self.__class__.__name__}(amqp={self.amqp}, loglevel={self.loglevel})"
