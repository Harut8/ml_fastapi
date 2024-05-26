from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, BackgroundTasks
from starlette.responses import FileResponse

from app.containers import DependencyContainer
from app.use_case.prediction.prediction import PredictionService
from app.use_case.prediction.prediction_dto import ActivePipelineDto
from app.use_case.prediction.prediction_schema import PredictionSource
from app.utils.cbv import cbv
from app.utils.response import Response
from ports.api.prediction import IPredictionApi

prediction_api = APIRouter()


@cbv(prediction_api)
class PredictionApi(IPredictionApi):

    @prediction_api.get("/source/file_name/file")
    @inject
    async def download_file(self,
                            source: PredictionSource,
                            file_name: str,
                            prediction_service: PredictionService = Depends(
                                Provide[DependencyContainer.prediction_service]
                            )) -> FileResponse:
        _file = await prediction_service.download_file(source, file_name)
        return _file

    @prediction_api.patch("/reset-train")
    async def reset_train(self):
        ...

    @prediction_api.get("/train-pipeline")
    @inject
    async def train_pipeline(self,
                             background_tasks: BackgroundTasks,
                             prediction_service: PredictionService = Depends(
                                 Provide[DependencyContainer.prediction_service]
                             )):
        background_tasks.add_task(prediction_service.training)
        return Response(status_code=200, message="Training started!")

    @prediction_api.get("/get-pipeline-status")
    @inject
    async def get_pipeline_status(self,
                                  prediction_service: PredictionService = Depends(
                                      Provide[DependencyContainer.prediction_service]
                                  )) -> ActivePipelineDto:
        _active_pipeline = await prediction_service.get_pipeline_status()
        return ActivePipelineDto(active_count=_active_pipeline)

    @prediction_api.get("/get-pipeline-details")
    @inject
    async def get_pipeline_details(self,
                                   prediction_service: PredictionService = Depends(
                                       Provide[DependencyContainer.prediction_service]
                                   )):
        return await prediction_service.get_pipeline_details()

    @prediction_api.get("/prediction-files")
    @inject
    async def get_prediction_files(self,
                                   prediction_service: PredictionService = Depends(
                                       Provide[DependencyContainer.prediction_service]
                                   )):
        return await prediction_service.get_prediction_files()
