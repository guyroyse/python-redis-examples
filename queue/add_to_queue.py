import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://:foobared@localhost:6379/0', encoding='utf-8')

  await asyncio.gather(
    add_to_queue(redis, 'Possible vocalizations east of Makanda'),
    add_to_queue(redis, 'Sighting near the Columbia River'),
    add_to_queue(redis, 'Chased by a tall hairy creature')
  )

  redis.close()
  await redis.wait_closed()

def add_to_queue(redis, message):
  return redis.rpush('bigfoot:sightings:received', message)

asyncio.run(main())
