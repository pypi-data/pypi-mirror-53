from .redis_manager import RedisManager

from aioredis import create_connection

'''
Create a new Redis connection.
:param string address
:param dict **kwargs
:returns RedisManager
'''
async def connect(address, **kwargs):
    connection = await create_connection(address, **kwargs)
    redis_manager = RedisManager(connection)
    return redis_manager
