import sys
import logging
import asyncio

logger = logging.getLogger("BloodCoinMainCore")

class CrawlBot:
    def __init__(self):
        self.is_alive = True
        self.loop = asyncio.get_event_loop()

    async def teardown(self):
        logging.warn(" ! TEARDOWN ! Event loop was died")

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.teardown())
        finally:
            self.loop.close()