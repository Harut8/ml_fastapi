import os
from datetime import datetime

from starlette.responses import FileResponse

from adapters.spi.base_repo import BaseRepository, transactional
from adapters.spi.dataset import DatasetRepository
from adapters.spi.prediction import PredictionRepository
from app.entity.prediction import Training
from app.exceptions.http_exceptions import NotFound
from app.use_case.base_use_case import BaseUseCase
from app.use_case.prediction.prediction_schema import PredictionSource
from app.utils.training_pipeline import TrainingPipeline


class PredictionService(BaseUseCase):
    def __init__(self,
                 base_repo: BaseRepository,
                 prediction_repo: PredictionRepository,
                 dataset_repo: DatasetRepository):
        self._base_repo = base_repo
        self._prediction_repo = prediction_repo
        self._dataset_repo = dataset_repo
        super().__init__(base_repo)

    def _get_created_datetime(self, file_path: str):
        created_datetime = os.path.getctime(file_path)
        modified_datetime = os.path.getmtime(file_path)
        created_datetime = datetime.fromtimestamp(created_datetime).strftime('%Y-%m-%d %H:%M:%S')
        modified_datetime = datetime.fromtimestamp(modified_datetime).strftime('%Y-%m-%d %H:%M:%S')
        return created_datetime, modified_datetime

    async def download_file(self, source, file_name) -> FileResponse:
        _file_path = source + file_name
        try:
            _full_path = f"{os.getcwd()}/{_file_path}"
            return FileResponse(_file_path, media_type="application/x-zip-compressed",
                                headers={'Content-Disposition': f'attachment; filename="{file_name}"'})
        except Exception:
            raise NotFound(message=f"File {file_name} not found")

    @transactional(commit_at_end=False)
    async def get_pipeline_details(self):
        return await self._prediction_repo.get_pipeline_details()

    @transactional(commit_at_end=False)
    async def get_pipeline_status(self):
        return await self._prediction_repo.get_pipeline_status()

    def delete_file(self, file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)

    def clear_all_models(self):
        folder = f"{os.getcwd()}/app/{PredictionSource.clustering_models.value}/"
        for files in os.listdir(folder):
            self.delete_file(folder + files)

    @transactional(commit_at_end=True)
    async def training(self):
        _training = Training(
            is_running=1,
            pipe_line_name="Training"
        )
        await self._prediction_repo.add_pipeline_details(_training)
        _default_dataset = await self._dataset_repo.def_default_dataset()
        _path = f"{os.getcwd()}/app/{PredictionSource.processed.value}/{_default_dataset.file_name}"
        self.clear_all_models()
        train_pipe = TrainingPipeline()
        train_pipe.train_model(_path)
        _training.is_running = 0
        return

    async def get_prediction_files(self):
        result = []
        prediction_path = f"{os.getcwd()}/app/{PredictionSource.prediction.value}/"
        for file in os.listdir(prediction_path):
            created_datetime, modified_datetime = self._get_created_datetime(prediction_path + file)
            record = {
                'file_name': file,
                'created_on': created_datetime
            }
            result.append(record)
        return result
