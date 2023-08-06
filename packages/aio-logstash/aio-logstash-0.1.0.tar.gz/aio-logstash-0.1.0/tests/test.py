import logging
import asyncio
from aio_logstash.handler import TCPHandler


async def main():
    handler = TCPHandler()
    await handler.connect('127.0.0.1', 5000)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info('test', extra={'foo': 'bar'})

    await handler.exit()


if __name__ == '__main__':
    asyncio.run(main())
