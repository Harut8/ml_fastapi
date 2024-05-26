from sqlalchemy import select, func

from adapters.spi.base_repo import BaseRepository
from app.entity.prediction import Training
from ports.spi.prediction import IPredictionRepository


class PredictionRepository(IPredictionRepository, BaseRepository[Training]):
    async def get_pipeline_details(self) -> list[Training]:
        _stmt = select(Training).order_by(Training.created_at.desc())
        _training = await self.run_select_stmt_for_all(_stmt)
        return list(_training)

    async def get_pipeline_status(self) -> int:
        _stmt = select(func.count(Training.is_running).label('activeCount')).where(Training.is_running == 1)
        _training = await self.run_select_stmt_for_one(_stmt)
        return _training  # type: ignore

    async def add_pipeline_details(self, training: Training) -> Training:
        await self.insert_one_without_commit(training)
        return training
