# Данная библиотека позволяет удобно работать с асинхронным Redis-хранилищем
Пример инициализации хранилища:
```python
from aioredis_storage import RedisStorage

storage = RedisStorage(
	db_name = 'localhost',
	db_port = 6379,
	db_number=1,
	db_password='foobared'
)

a = list('123')
# ['1', '2', '3']
await storage.set_data(address = 'str_addr', a)

await storage.get_data(address = 'str_addr')
# ['1', '2', '3']

```


## Своя пре и пост обработка данных
Данный пример позволяет хранить все данные сериализованными pickle
```python
from aioredis_storage.mixins import AbstractMixin
from aioredis_storage.storage import AbstractRedisStorage

class PickleMixin(AbstractMixin):

	async def load(self, data) -> object:
		return pickle.loads(data)

	async def dump(self, data) -> str:
		return pickle.dumps(data)


class RedisPickleStorage(AbstractRedisStorage, PickleMixin):
	pass

```

По умолчанию хранилище работает с `PickleMixin`, но вы можете использовать `JSONMixin`, `BaseMixin` при необходимости.
