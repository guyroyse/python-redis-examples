import asyncio
import aioredis

from pprint import pp

async def main():

  redis = await aioredis.create_redis('redis://:foobared@localhost:6379/0', encoding='utf-8')

  await redis.execute('FT.DROP', 'bigfoot:sightings:search')

  await redis.execute('FT.CREATE', 'bigfoot:sightings:search',
    'SCHEMA', 'title', 'TEXT', 'classification', 'TEXT')

  await asyncio.gather(
    add_document(redis, 1, 'Possible vocalizations east of Makanda', 'Class B'),
    add_document(redis, 2, 'Sighting near the Columbia River', 'Class A'),
    add_document(redis, 3, 'Chased by a tall hairy creature', 'Class A'))

  results = await search(redis, 'chase|east')
  pp(results)

  redis.close()
  await redis.wait_closed()

def add_document(redis, id, title, classification):
  return redis.execute('FT.ADD', 'bigfoot:sightings:search', id, '1.0',
    'FIELDS', 'title', title, 'classification', classification)

def search(redis, query):
  return redis.execute('FT.SEARCH', 'bigfoot:sightings:search', query)

asyncio.run(main())
