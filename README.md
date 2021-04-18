# Данная библиотека позволяет удобно работать с асинхронный Redis-хранилищем.
Пример инициализации хранилища:
```
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
