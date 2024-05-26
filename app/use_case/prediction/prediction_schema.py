from enum import StrEnum


class PredictionSource(StrEnum):
    prediction = "prediction_results"
    processed = "processed_files"
    validation_path = 'validation_files'
    clustering_models = 'clustering_models'

