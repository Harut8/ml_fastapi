from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile, File

from app.containers import DependencyContainer
from app.use_case.dataset.dataset import DatasetService
from app.use_case.dataset.dataset_dto import DatasetDto
from app.utils.cbv import cbv
from app.utils.response import Response
from ports.api.dataset import IDatasetApi

dataset_api = APIRouter()


@cbv(dataset_api)
class DatasetApi(IDatasetApi):

    @dataset_api.get("/dataset-list")
    @inject
    async def get_dataset_list(self,
                               dataset_service: DatasetService = Depends(
                                   Provide[DependencyContainer.dataset_service])) -> list[DatasetDto]:
        return await dataset_service.get_dataset_list()

    @dataset_api.get("/default-dataset")
    @inject
    async def get_default_dataset(self,
                                  dataset_service: DatasetService = Depends(
                                      Provide[DependencyContainer.dataset_service])) -> list[DatasetDto]:
        return await dataset_service.get_default_data_set_list()

    @dataset_api.patch("/default-dataset")
    @inject
    async def update_default_dataset(self,
                                     file_name: str,
                                     dataset_service: DatasetService = Depends(
                                         Provide[DependencyContainer.dataset_service])
                                     ):
        await dataset_service.update_default_dataset(file_name)
        return Response(status_code=200, message="Updated successfully!")

    @dataset_api.post("/data-file")
    @inject
    async def upload_data(self,
                          data_file: UploadFile = File(...),
                          dataset_service: DatasetService = Depends(
                              Provide[DependencyContainer.dataset_service])
                          ):
        await dataset_service.upload_data(data_file)
        return Response(status_code=200, message="Uploaded successfully!")
