

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
