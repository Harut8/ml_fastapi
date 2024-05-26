from abc import ABC, abstractmethod

from app.entity.prediction import Training


class IPredictionRepository(ABC):
    @abstractmethod
    async def get_pipeline_details(self) -> list[Training]:
        ...

    @abstractmethod
    async def get_pipeline_status(self) -> list[Training]:
        ...

    @abstractmethod
    async def add_pipeline_details(self, training: Training) -> Training:
        ...
