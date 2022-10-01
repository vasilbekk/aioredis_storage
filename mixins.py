import json
import pickle
from abc import ABC, abstractmethod


class AbstractMixin(ABC):
    """
    Абстрактный класс для наследования
    И создания новых способов обработки данных
    """

    @abstractmethod
    async def load(self, data):
        """
        Получает данные, возвращенные хранилищем
        Возвращает обаботанные данные.

        Вызывается после того, как данные были получены из хранилища
        """
        raise NotImplementedError

    @abstractmethod
    async def dump(self, data):
        """
        Получает данные, котороые необходимо преобразовать
        Возвращает преобразованные данные для хранилища.

        Вызывается перед тем, как положить данные в хранилище
        """
        raise NotImplementedError


class BaseMixin(AbstractMixin):
    async def load(self, data):
        return data

    async def dump(self, data):
        return data


class JSONMixin(AbstractMixin):
    async def load(self, data) -> object:
        return json.loads(data)

    async def dump(self, data) -> str:
        return json.dumps(data)


class PickleMixin(AbstractMixin):
    async def load(self, data) -> object:
        return pickle.loads(data)

    async def dump(self, data) -> str:
        return pickle.dumps(data)
