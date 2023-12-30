from abc import ABC, abstractmethod




class AbstactDAO(ABC):
    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none():
        raise NotImplementedError

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class IUnitOfWork:

    def __init__(self) -> None:
        ...

    async def __aenter__(self):
        ...

    async def __aexit__(self, *args):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...
