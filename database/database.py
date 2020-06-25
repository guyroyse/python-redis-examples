import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://:foobared@localhost:6379/0', encoding='utf-8')

  await asyncio.gather(
    add_sighting(redis, 1, 'Possible vocalizations east of Makanda', 'Class B'),
    add_sighting(redis, 2, 'Sighting near the Columbia River', 'Class A'),
    add_sighting(redis, 3, 'Chased by a tall hairy creature', 'Class A'))
  
  sightings = await asyncio.gather(
    read_sighting(redis, 1),
    read_sighting(redis, 2),
    read_sighting(redis, 3))

  pp(sightings)

  redis.close()
  await redis.wait_closed()

def add_sighting(redis, id, title, classification):
  return redis.hmset(f'bigfoot:sighting:{id}',
    'id', id, 'title', title, 'classification', classification)

def read_sighting(redis, id):
  return redis.hgetall(f'bigfoot:sighting:{id}')

asyncio.run(main())
