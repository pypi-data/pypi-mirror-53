# -*- coding: utf-8 -*-

"""The WCraaS Storage module is responsible for providing storage services for the platform."""

import asyncio
import json
import logging
import aio_pika

from aio_pika import connect_robust, IncomingMessage, ExchangeType
from aio_pika.patterns import RPC
from aio_pika.pool import Pool
from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient

from wcraas_common import AMQPConfig, WcraasWorker
from wcraas_storage.config import MongoConfig


class StorageWorker(WcraasWorker):
    def __init__(self, amqp: AMQPConfig, mongo: MongoConfig, mapping: Dict[str, str], loglevel: int, *args, **kwargs):
        super().__init__(amqp, loglevel)
        self.mongo = mongo
        self.logger = logging.getLogger("wcraas.storage")
        self.logger.setLevel(loglevel)
        self._db = AsyncIOMotorClient(mongo.host, mongo.port)[mongo.db]
        self._close = asyncio.Event()
        self.mapping = mapping

    async def store(self, message: IncomingMessage) -> None:
        """
        AMQP consumer function, that inserts an `IncomingMessage`'s json-loaded body in a MongoDB collection based on the source exchange.

        :param message: The message that trigered the consume callback.
        :type message: aio_pika.IncomingMessage
        """
        async with message.process():
            try:
                result = await self._db[self.mapping[message.exchange]].insert_one(json.loads(message.body))
                self.logger.info(result)
            except Exception as err:
                self.logger.error(err)

    async def start(self) -> None:
        """
        Asynchronous runtime for the worker, responsible of managing and maintaining async context open.
        """
        async with self._amqp_pool.acquire() as sub_channel:
            await sub_channel.set_qos(prefetch_count=1)
            for queue_name, collection in self.mapping.items():
                exchange = await sub_channel.declare_exchange(queue_name, ExchangeType.FANOUT)
                queue = await sub_channel.declare_queue(exclusive=True)
                await queue.bind(exchange)
                await queue.consume(self.store)
                self.logger.info(f"Registered {queue_name} ...")
            await self._close.wait()

    def run(self) -> None:
        """
        Helper function implementing the synchronous boilerplate for initilization and reardown.
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.logger.info("[x] Received ^C ! Exiting ...")
        finally:
            self._close.set()
            loop.shutdown_asyncgens()
