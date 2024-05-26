from sqlalchemy import select, insert

from adapters.spi.base_repo import BaseRepository
from app.entity.dataset import DefaultDataset
from ports.spi.dataset import IDatasetRepository


class DatasetRepository(IDatasetRepository, BaseRepository[DefaultDataset]):

    async def get_default_data_set_list(self) -> list[DefaultDataset]:
        _stmt = select(DefaultDataset).order_by(DefaultDataset.created_at.desc())
        _default_dataset = await self.run_select_stmt_for_all(_stmt)
        return list(_default_dataset)

    async def def_default_dataset(self) -> DefaultDataset:
        _stmt = select(DefaultDataset).where(DefaultDataset.uuid == "2ccacfe9-b825-48bb-8acf-e9b825e8bb97")
        _default_dataset = await self.run_select_stmt_for_one(_stmt)
        return _default_dataset
