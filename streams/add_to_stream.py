import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://:foobared@localhost:6379/0', encoding='utf-8')

  await asyncio.gather(
    add_to_stream(redis, 1, 'Possible vocalizations east of Makanda', 'Class B'),
    add_to_stream(redis, 2, 'Sighting near the Columbia River', 'Class A'),
    add_to_stream(redis, 3, 'Chased by a tall hairy creature', 'Class A'))

  redis.close()
  await redis.wait_closed()

def add_to_stream(redis, id, title, classification):
  return redis.xadd('bigfoot:sightings:stream', {
    'id': id, 'title': title, 'classification': classification })

asyncio.run(main())
