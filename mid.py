from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse
from training_pipeline import TrainingPipeline
from prediction import Prediction
import utils as util
import os
import shutil
import uvicorn
import sqlite3

app = FastAPI()
origins = ["*"]
processed_path = 'Processed_Files/'
prediction_path = 'Prediction_Results/'
validation_path = 'Validation_Files/'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Datasets(BaseModel):
    file_name: str
    created_on: str
    last_modified: str
    file_name: str


class DownloadFile(BaseModel):
    file_name: str
    source: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_prediction_files_list")
async def get_prediction_files_list():
    result = []
    for file in os.listdir(prediction_path):
        created_datetime, modified_datetime = util.get_created_datetime(prediction_path + file)
        record = {
            'file_name': file,
            'created_on': created_datetime
        }
        result.append(record)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
