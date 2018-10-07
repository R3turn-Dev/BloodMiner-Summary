import os
import asyncio
import logging
import aiohttp
import datetime as dtime

from core import CrawlBot
from logger import DBLogger
from settings import Config

# Retrieve Settings
_settings = Config()
_chain_settings = _settings.get("Chain")
_bot_settings = _settings.get("Bot")
_db_settings = _settings.get("Database")


# Setup Logger
logger = logging.getLogger("BloodCoinMainCore")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(levelname)-8s] %(filename)s => %(asctime)s | %(message)s")


# Make Bot Client
client = CrawlBot()


async def timer():
    CheckInterval = _bot_settings.get("check_interval")

    logger.info(" * Checking web every " + str(CheckInterval) + " Seconds")
    dbLogger = DBLogger(_db_settings)
    
    UpcomingUpdate = dtime.datetime.now()
    UpcomingUpdate = UpcomingUpdate.replace(
        second=0,
        microsecond=0
    ) + dtime.timedelta(seconds=CheckInterval)

    LastSeek = ""

    while client.is_alive:
        await asyncio.sleep(0.1)
        if UpcomingUpdate < dtime.datetime.now():
            UpcomingUpdate += dtime.timedelta(seconds=CheckInterval)

            try:
                async with aiohttp.ClientSession() as Session:
                    async with Session.get(_chain_settings.get("summary_uri")) as req:
                        LastSeek = await req.text()
                        result = await req.json()

                        dbLogger.write_log(result['data'])
                        logger.debug(str(result))
                        
            except Exception as ex:
                logger.warn(repr(ex))
                logger.warn("Meta " + repr(LastSeek))


client.loop.create_task(timer())
client.run()
