from starlette import status

from app.exceptions.http_exceptions import ServiceException


class FileProcessingError(ServiceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "File Processing Error"
    code = "FILE_PROCESSING_ERROR"
