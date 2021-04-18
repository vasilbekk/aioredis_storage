from abc import ABC
from typing import Any

import aioredis

from .mixins import JSONMixin, PickleMixin


class AbstractRedisStorage(ABC):

	def __init__(self,
				db_name: str = 'localhost',
				db_port: int = 6379,
				db_number: int = None,
				password: int = None):
		self._name = db_name
		self._port = db_port
		self._number = db_number
		self._password = password
		self._redis = None

	async def redis(self):
		if not self._redis:
			self._redis = await aioredis.create_connection(
				(self._name, self._port),
				db = self._number,
				password = self._password
				)

		return self._redis

	async def set_data(self, address: str, data: Any):
		conn = await self.redis()
		data = await self.dump(data)
		await conn.execute('SET', address, data)

	async def get_data(self, address: str):
		conn = await self.redis()

		raw_data = await conn.execute('GET', address)
		data = await self.load(raw_data)
		return data


class RedisStorage(AbstractRedisStorage, PickleMixin):
	pass

class RedisJSONStorage(AbstractRedisStorage, JSONMixin):
	pass
