from abc import ABC, abstractmethod


class IDatasetRepository(ABC):

    @abstractmethod
    async def get_default_data_set_list(self):
        ...
