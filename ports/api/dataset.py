from typing import Protocol


class IDatasetApi(Protocol):
    async def get_dataset_list(self):
        ...

    async def get_default_dataset(self):
        ...

    async def update_default_dataset(self, file_name):
        ...

    async def upload_data(self, data_file: UploadFile):
        ...
