from abc import ABC
from typing import Any, List

import aioredis

from .mixins import JSONMixin, PickleMixin

DEFAULT_PREFIX = "rs"
DEFAULT_SEPARATOR = ":"


class AbstractRedisStorage(ABC):
    def __init__(
        self,
        db_name: str = "localhost",
        db_port: int = 6379,
        db_number: int = None,
        password: int = None,
        prefix: str = DEFAULT_PREFIX,
        separator: str = DEFAULT_SEPARATOR,
    ):
        self._name = db_name
        self._port = db_port
        self._number = db_number
        self._password = password
        self._prefix = prefix
        self._separator = separator
        self._redis = None

    async def redis(self):
        if not self._redis:
            self._redis = await aioredis.create_connection(
                (self._name, self._port), db=self._number, password=self._password
            )

        return self._redis

    async def close(self):
        if self._redis and not self._redis.closed:
            self._redis.close()

    async def get_address(self, key: str) -> str:
        return "%s%s%s" % (self._prefix, self._separator, key)

    async def set_data(self, key: str, data: Any):
        conn = await self.redis()
        await conn.execute("SET", await self.get_address(key), await self.dump(data))

    async def get_data(self, key: str):
        conn = await self.redis()
        raw_data = await conn.execute("GET", await self.get_address(key))
        return await self.load(raw_data)

    async def all_keys(self):
        conn = await self.redis()
        keys = await conn.execute("KEYS", f"{self._prefix}:*")
        result = []
        for key in keys:
            *_, key = key.decode("utf-8").split(self._separator)
            result.append(key)

        return result

    async def reset_all(self, full=False) -> List[str]:
        conn = await self.redis()

        if full:
            await conn.execute("FLUSHDB")
        else:
            addr = await self.get_address("*")
            keys = await conn.execute("KEYS", addr)
            await conn.execute("DEL", *keys)

        return keys

    async def reset(self, *keys):
        conn = await self.redis()
        await conn.execute("DEL", *keys)


class RedisStorage(AbstractRedisStorage, PickleMixin):
    pass


class RedisJSONStorage(AbstractRedisStorage, JSONMixin):
    pass
