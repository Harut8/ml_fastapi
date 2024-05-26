from abc import ABC, abstractmethod


class IPostgresDB(ABC):
    @abstractmethod
    async def session_dependency(self):
        pass

    @abstractmethod
    async def scoped_session_dependency(self):
        pass

    @abstractmethod
    def get_async_scoped_session(self):
        pass

    @abstractmethod
    async def session(self):
        pass
