import functools
from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.entity.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class IBaseRepository(Generic[T], ABC):

    @abstractmethod
    def factory(cls: type, **kwargs):
        ...

    @property
    @abstractmethod
    def db(self):
        ...

    @property
    @abstractmethod
    def session(self):
        ...

    @session.setter
    @abstractmethod
    def session(self, session: AsyncSession):
        ...

    @staticmethod
    @abstractmethod
    async def _insert_instance(instance: T, db: AsyncSession):
        ...

    @abstractmethod
    async def run_select_stmt_for_one(self, stmt) -> T:
        ...

    @abstractmethod
    async def run_select_stmt_for_all(self, stmt) -> list[T]:
        ...

    @abstractmethod
    async def insert_one_with_commit(self, instance: T):
        ...

    @abstractmethod
    async def insert_one_without_commit(self, instance: T):
        ...

    @abstractmethod
    async def insert_many_orm_with_commit(self, instances: list[T]):
        ...

    @abstractmethod
    async def insert_many_orm_without_commit(self, instances: list[T]):
        ...

    @abstractmethod
    async def bulk_insert_core_without_commit(self, instances: list[dict], mapping):
        ...

    @abstractmethod
    async def del_exist_instance(self, instance: T):
        ...

    @abstractmethod
    async def del_exist_instances(self, instances: list[T]):
        ...

    @abstractmethod
    async def del_exist_instance_without_commit(self, instance: T):
        ...

    @abstractmethod
    async def del_exist_instances_without_commit(self, instances: list[T]):
        ...

    @abstractmethod
    async def update_instance(self, instance: T):
        ...

    @abstractmethod
    async def update_instance_without_commit(self, instance: T):
        ...

    @abstractmethod
    async def update_instances(self, instances: list[T]):
        ...

    @abstractmethod
    async def update_instances_without_commit(self, instances: list[T]):
        ...

    @abstractmethod
    async def update_stmt(self, stmt):
        ...
