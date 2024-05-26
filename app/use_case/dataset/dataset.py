import os
import shutil
from datetime import datetime

from fastapi import UploadFile

from adapters.spi.base_repo import BaseRepository, transactional
from adapters.spi.dataset import DatasetRepository
from app.use_case.base_use_case import BaseUseCase
from app.use_case.dataset.dataset_dto import DatasetDto
from app.use_case.prediction.prediction_schema import PredictionSource
from app.utils.ml_prediction import Prediction


class DatasetService(BaseUseCase):

    def __init__(self,
                 base_repo: BaseRepository,
                 dataset_repo: DatasetRepository):
        self._base_repo = base_repo
        self._dataset_repo = dataset_repo
        super().__init__(base_repo)

    def _get_created_datetime(self, file_path: str):
        created_datetime = os.path.getctime(file_path)
        modified_datetime = os.path.getmtime(file_path)
        created_datetime = datetime.fromtimestamp(created_datetime).strftime('%Y-%m-%d %H:%M:%S')
        modified_datetime = datetime.fromtimestamp(modified_datetime).strftime('%Y-%m-%d %H:%M:%S')
        return created_datetime, modified_datetime

    async def get_dataset_list(self) -> list[DatasetDto]:
        result = []
        _processed_path = f"{os.getcwd()}/app/{PredictionSource.processed.value}/"
        for file in os.listdir(_processed_path):
            created_datetime, modified_datetime = self._get_created_datetime(_processed_path + file)
            record = {
                'file_name': file,
                'created_at': created_datetime,
                'updated_at': modified_datetime
            }
            result.append(DatasetDto(**record))
        return result

    @transactional(commit_at_end=False)
    async def get_default_data_set_list(self) -> list[DatasetDto]:
        _dataset_list = await self._dataset_repo.get_default_data_set_list()
        return [DatasetDto.model_validate(_dataset) for _dataset in _dataset_list]

    @transactional(commit_at_end=True)
    async def update_default_dataset(self, file_name: str):
        _default_dataset = await self._dataset_repo.def_default_dataset()
        _default_dataset.file_name = file_name

    def delete_file(self, file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)

    async def upload_data(self, data_file: UploadFile):
        _path = f"{os.getcwd()}/app/{PredictionSource.validation_path.value}/{data_file.filename}"
        self.delete_file(_path)
        with open(_path, "wb+") as file_object:
            shutil.copyfileobj(data_file.file, file_object)
        predict_pipe = Prediction()
        predict_pipe.prediction(_path)
