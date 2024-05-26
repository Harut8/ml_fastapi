from typing import Protocol

from fastapi import BackgroundTasks
from starlette.responses import FileResponse

from app.use_case.prediction.prediction_schema import PredictionSource


class IPredictionApi(Protocol):
    async def download_file(self, source: PredictionSource, file_name: str) -> FileResponse:
        ...

    async def reset_train(self):
        ...

    async def train_pipeline(self, background_tasks: BackgroundTasks):
        ...

    async def get_pipeline_status(self):
        ...

    async def get_pipeline_details(self):
        ...

    async def get_prediction_files_list(self):
        ...
