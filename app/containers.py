from dependency_injector import containers, providers

from adapters.spi.base_repo import BaseRepository
from adapters.spi.dataset import DatasetRepository
from adapters.spi.postgres import PostgresDB
from adapters.spi.prediction import PredictionRepository
from app.settings import APP_SETTINGS
from app.use_case.dataset.dataset import DatasetService
from app.use_case.prediction.prediction import PredictionService


class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "adapters.api.dataset",
            "adapters.api.prediction",
            "app.use_case.dataset.dataset",
            "app.use_case.prediction.prediction",
        ]
    )
    db = providers.Singleton(PostgresDB, url=APP_SETTINGS.DATABASE.POSTGRES_DSN)
    base_repo = providers.Factory(BaseRepository, db=db.provided.session)
    dataset_repo = providers.Singleton(DatasetRepository, db=db.provided.session)
    prediction_repo = providers.Singleton(PredictionRepository, db=db.provided.session)
    prediction_service = providers.Factory(
        PredictionService,
        base_repo=base_repo,
        prediction_repo=prediction_repo,
        dataset_repo=dataset_repo
    )
    dataset_service = providers.Factory(
        DatasetService,
        base_repo=base_repo,
        dataset_repo=dataset_repo
    )
