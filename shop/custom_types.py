from rest_framework import status
import dataclasses

from .constants import STATUS_400_ERROR_TEXT, STATUS_404_ERROR_TEXT


@dataclasses.dataclass
class Error:
    code: int
    message: str

    def to_dict(self):
        return {'code': self.code, 'message': self.message}


ERROR_400: Error = Error(status.HTTP_400_BAD_REQUEST, STATUS_400_ERROR_TEXT)
ERROR_404: Error = Error(status.HTTP_404_NOT_FOUND, STATUS_404_ERROR_TEXT)
