import sys
import logging
import asyncio
from logger import DiscordLogger as DLogger
from settings import Config

logger = logging.getLogger("BloodCoinMainCore")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)-8s] %(filename)s => %(asctime)s | %(message)s")

HookConfig = Config().get("Hook")
DiscordLogger = DLogger(HookConfig)
DiscordLogger.setFormatter(formatter)
DiscordLogger.setLevel(logging.WARNING)
logger.addHandler(DiscordLogger)

class CrawlBot:
    def __init__(self):
        self.is_alive = True
        self.loop = asyncio.get_event_loop()

    async def teardown(self):
        logger.warn(" ! TEARDOWN ! Event loop was died")

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.teardown())
        finally:
            self.loop.close()